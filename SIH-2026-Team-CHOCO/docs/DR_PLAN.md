# SIH26184 — Disaster Recovery Plan

> Checklist §19.7 deliverable. Aligned with `docker-compose.yml` (2026-09-05).

## Architecture Recap

5 compose services (`docker-compose.yml`):

| Service | Image | Persistence | Health Check |
|---------|-------|-------------|--------------|
| `backend` | `deployments/Dockerfile.backend` | — (stateless) | `curl http://localhost:8000/health` (30s interval) |
| `postgres` | `postgres:16-alpine` | `postgres_data` | `pg_isready -U sih_admin -d sih26184_app` |
| `neo4j` | `neo4j:5-community` | `neo4j_data`, `neo4j_logs` | `wget http://localhost:7474` |
| `redis` | `redis:7-alpine` | `redis_data` | `redis-cli ping` |
| `celery-worker` | `deployments/Dockerfile.backend` | — | — |

All services: `restart: unless-stopped`.

## Backup Matrix

| Asset | Script | Method | Schedule | Retention | Output |
|-------|--------|--------|----------|-----------|--------|
| PostgreSQL | `scripts/postgresql_backup.sh` | `pg_dump -Fc` (custom format) | Daily 02:00 cron | 7 days | `backups/${DB}_<TS>.dump` |
| Neo4j | `scripts/neo4j_backup.sh` | `neo4j-admin database dump` via container | Daily 03:00 cron | 7 days | `backups/neo4j_dump_<TS>.dump` |
| Full stack | `scripts/backup.sh` | `pg_dump` (plain SQL) + `neo4j-admin dump` + `redis-cli SAVE` (RDB) | Manual / cron | — | `backups/postgres_<TS>.sql`, `backups/redis_<TS>.rdb` |
| Redis AOF | `docker-compose.yml` | `appendonly yes` (AOF replay) | Continuous | — | `redis_data` volume |
| Blockchain | `scripts/blockchain_init.py` | Genesis block recreation | On init | — | `audit_logs` table |

**Cron entries (suggested):**

```cron
0 2 * * * /path/to/scripts/postgresql_backup.sh
0 3 * * * /path/to/scripts/neo4j_backup.sh
```

## RTO / RPO Targets

| Metric | Target | Basis |
|--------|--------|-------|
| RPO | ≤ 24h | Daily dumps |
| RTO | ≤ 4h | `docker compose up` + `alembic upgrade head` + seeds + `blockchain_init.py` |

> Note: SIH.md §22 claimed "backups every 6h" — actual schedule is **daily**. See §19.7 backup matrix above.

## Failure Drills

| Failure | Behavior | Recovery |
|---------|----------|----------|
| PostgreSQL down | `/health` → `degraded`, app proceeds (DB routes return 503) | Restart postgres container, verify `pg_isready` |
| Neo4j down | Graph queries degrade gracefully | Restart neo4j, verify `wget http://localhost:7474` |
| Redis down | Rate limiting + blacklist skipped, requests proceed (warning log) | Restart redis, AOF replays automatically |
| Full-stack loss | All services down | Follow "Full Restore" runbook below |

## Restore Runbooks

### PostgreSQL

```bash
# Using postgresql_backup.sh dumps (custom-format):
export PGPASSWORD="$POSTGRES_PASSWORD"
pg_restore -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" --clean --if-exists backups/sih26184_app_<TS>.dump

# Using backup.sh dumps (plain SQL):
psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" < backups/postgres_<TS>.sql

# Or via restore.sh (auto-picks latest):
bash scripts/restore.sh ./backups latest
```

### Neo4j

```bash
# Requires Neo4j stopped:
docker stop <NEO4J_CONTAINER>
# Copy dump into container's backup path:
docker cp backups/neo4j_dump_<TS>.dump <NEO4J_CONTAINER>:/data/backup/neo4j.dump
docker exec <NEO4J_CONTAINER> neo4j-admin database load neo4j --from-path=/data/backup --overwrite-destination
docker start <NEO4J_CONTAINER>
```

### Redis

```bash
# AOF replays automatically on restart (appendonly yes):
docker compose restart redis

# Manual RDB restore (from backup.sh):
docker compose cp backups/redis_<TS>.rdb redis:/data/dump.rdb
docker compose restart redis
```

### Full Restore (zero-to-running)

```bash
docker compose up -d
# Wait for health checks:
docker compose ps   # all healthy
alembic upgrade head
python scripts/postgresql_seed_data.py   # or psql < scripts/postgresql_seed_data.sql
python scripts/neo4j_populate.py
python scripts/blockchain_init.py        # genesis block (skips if rows exist)
curl http://localhost:8000/health        # verify: {"status":"healthy","services":{"api":"healthy",...}}
```

## Encryption & Key Management

> **Critical:** PII in `victims` and `complaints` (BYTEA columns) was encrypted with `PG_ENCRYPTION_KEY` (SHA-256 → AES-256-GCM, `api/security/encryption.py`). A backup restores the **ciphertext**, not the plaintext. The **same `PG_ENCRYPTION_KEY`** must be set on the restore target or every PII field is unrecoverable. Rotate keys only with a planned re-encryption migration.

- Backups must not be assumed readable without the matching `PG_ENCRYPTION_KEY`.
- IPFS evidence blobs are likewise encrypted with the same key before upload (`api/services/ipfs.py:24-29`).

## Incident Response Checklist

1. **Detect** — `GET /health` (status `degraded` + per-service breakdown), compose `healthcheck` logs, monitoring dashboards.
2. **Contain** — Isolate affected service (`docker compose stop <svc>`), disable ingress if data at risk.
3. **Restore** — Follow the runbook for the failed service above; for full loss use "Full Restore".
4. **Verify** — `GET /health` → `healthy`; row counts (`SELECT count(*) FROM complaints;`); blockchain integrity via `GET /api/v1/blockchain/verify/{complaint_id}` (`{verified:true, block_count, broken_at:null}`); spot-check PII decrypt round-trip.

## Known Gaps

- `scripts/neo4j_backup.sh` default container name is `sih-neo4j` — override with `NEO4J_CONTAINER` env.
- `scripts/backup.sh` uses `exec -T` (no TTY) and falls back gracefully if Neo4j console dump is unavailable.
- `scripts/restore.sh` restores Postgres + Redis only (Neo4j restore requires the service stopped — see runbook above).
