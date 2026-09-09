# SIH26184 — Judge Q&A Preparation (Member 2)

> Checklist §22 deliverable. Demo-day prep for the backend presenter.

## The 10 Questions (from SIH.md §22, lines 1122-1162)

### 1. "Why Neo4j over a relational database?"

Fraud networks are inherently graph structures. Neo4j lets us traverse transaction chains and mule networks in milliseconds with graph-specific traversal, whereas SQL would need expensive recursive JOINs over the same edges. The graph model also mirrors how investigators reason about a fraud — nodes and relationships — rather than forcing it into normalized tables.

*Evidence: `scripts/neo4j_queries.cypher`, `api/database/neo4j.py`, `docs/neo4j_schema.md`*

### 2. "How do you ensure data privacy?"

All PII in PostgreSQL is encrypted at rest using AES-256-GCM with a key derived from `PG_ENCRYPTION_KEY` — victim name, phone, bank account, and fraudster account are stored as ciphertext BYTEA. Neo4j holds only anonymized account identifiers, and the blockchain layer stores only SHA-256 hashes of audit actions. Evidence files are encrypted before they ever reach IPFS.

*Evidence: `api/security/encryption.py`, `docs/postgresql_schema.md:173-181`, `api/services/ipfs.py:24-29`, `api/services/blockchain.py:19-26`*

### 3. "What about database scalability?"

Every service is containerized and can scale horizontally — the backend, PostgreSQL, Neo4j, Redis, and Celery workers all run as independent compose services with persistent volumes. PostgreSQL supports partitioning and read replicas; Neo4j supports clustering; Redis handles caching and token blacklist state, all with per-service limits tuned in `docker-compose.yml`.

*Evidence: `docker-compose.yml`, `api/tasks/celery_app.py`, `api/database/redis.py`*

### 4. "How fast is the end-to-end pipeline?"

From complaint submission to ATM alert the pipeline runs in under 2 minutes: the complaint is persisted, mule and ATM predictions are dispatched to Celery workers, and the result is pushed back over WebSocket. The `/health` endpoint responds in ~1.1 seconds with all probes run concurrently and bounded to 1 second each.

*Evidence: `api/main.py:138-172`, `api/tasks/scoring.py`, `api/websocket/`, `Context.md:48,93`*

### 5. "How do you handle database failures?"

We run automated backups — daily PostgreSQL dumps at 02:00, daily Neo4j dumps at 03:00, Redis AOF persistence, and a restorable full-stack script. On failure the API degrades gracefully: `/health` reports `degraded` honestly instead of a false healthy, and dependent routes fail cleanly (503) rather than with tracebacks. Full-stack recovery is `docker compose up` + `alembic upgrade head` + seeds + blockchain genesis.

*Evidence: `scripts/postgresql_backup.sh`, `scripts/neo4j_backup.sh`, `scripts/backup.sh`, `scripts/restore.sh`, `api/main.py:38-57`, `docs/DR_PLAN.md`*

### 6. "What about fraudsters detecting the graph?"

The graph database is internal and never exposed to the public. Every external-facing API request is authenticated (JWT + RBAC) and rate-limited via the Redis sliding-window middleware (100 req/min per user, 1000/min per IP), so there is no unauthenticated or unthrottled path to probe the analytics backend.

*Evidence: `api/middleware/rate_limit.py`, `api/auth/rbac.py:28-46`*

### 7. "How do you ensure data integrity?"

Every sensitive action is written to the `audit_logs` table and chained into a SHA-256 blockchain — each block carries a `data_hash` and `previous_hash`, and the chain can be verified end-to-end via `GET /api/v1/blockchain/verify/{complaint_id}`. All writes use ACID transactions, and every request body is validated and sanitized before it reaches the database.

*Evidence: `api/services/blockchain.py:77-163`, `api/routes/blockchain.py`, `api/security/validation.py`, `api/main.py:185-190`*

### 8. "What about GDPR / Data Protection?"

All data is stored in India on our own infrastructure (local Docker volumes, no foreign SaaS for primary storage). PII is encrypted at rest, and our retention policy is defined: 5 years for complaints, 1 year for audit logs, with support for user data-deletion requests.

*Evidence: `docker-compose.yml` (local volumes), `docs/postgresql_schema.md` (encryption section), `api/security/encryption.py`*

### 9. "How do you handle API versioning?"

We use URL-based versioning — every route lives under `/api/v1/` (12 routers, 44 paths), enforced by a test that fails on any unversioned route. The OpenAPI spec is generated at `/api/openapi.json` and interactive docs at `/docs`.

*Evidence: `docs/API.md:3`, `api/main.py:216-248`, `tests/test_api_endpoints.py:104-108`*

### 10. "What about third-party integrations?"

WhatsApp via Meta Cloud API, email via SendGrid, SMS via Twilio, and IPFS via Pinata — each integration is mock-first in development and has a graceful fallback path when the real service is unavailable (e.g., IPFS falls back to a deterministic mock CID, and the WebSocket push keeps working).

*Evidence: `api/services/ipfs.py:44-71`, `api/services/whatsapp.py`, `api/services/notifications.py`, `api/config.py:74-83`*

## Demo Script

Decisive flow — Victim → complaint → heatmap → inspector verification → field alert → resolve.

### Setup

```bash
# Backend + DBs (all five compose services):
docker compose up -d

# Database bootstrap (if not yet run):
alembic upgrade head
python scripts/postgresql_seed_data.py   # or: psql < scripts/postgresql_seed_data.sql
python scripts/neo4j_populate.py
python scripts/blockchain_init.py
```

### Demo Creds

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| Inspector | `inspector1` | `inspector123` |
| Constable | `constable1` | `constable123` |

(Also seeded: `inspector2` / `constable2` with the same passwords.)

### Flow (API calls, from `docs/API.md`)

1. **Victim submits a complaint**
   ```
   POST /api/v1/victim/complaint
   ```
   Victim-supplied fields (name, phone, amount, fraud_type, upi, account). PII encrypted at write.

2. **Victim uploads evidence (optional)**
   ```
   POST /api/v1/victim/evidence
   ```
   Validated (10MB, extension + magic bytes), AES-256-GCM encrypted, uploaded to IPFS.

3. **Victim tracks status**
   ```
   GET /api/v1/victim/status/{complaint_id}
   ```

4. **Inspector logs in and reviews**
   ```
   POST /api/v1/auth/login            # inspector1 / inspector123
   GET /api/v1/police/complaints      # list complaints
   GET /api/v1/police/complaint/{complaint_id}
   ```
   Inspector sees the field-alert heatmap for withdrawal prediction:
   ```
   GET /api/v1/police/atms/heatmap    # high-probability ATMs
   GET /api/v1/police/atms/high-risk
   ```

5. **Inspector triggers step-up verification (field alert)**
   ```
   POST /api/v1/banking/step-up-verification
   GET  /api/v1/banking/verification/{verification_id}
   POST /api/v1/predict/trigger/verification
   ```

6. **Constable / inspector act**
   ```
   PUT  /api/v1/police/complaint/{complaint_id}/status   # → ACTION_TAKEN
   POST /api/v1/police/freeze/request                   # freeze fraudster funds
   POST /api/v1/police/fir/generate                     # FIR on record
   ```

7. **Resolve and verify integrity**
   ```
   PUT  /api/v1/police/complaint/{complaint_id}/status   # → RESOLVED
   GET  /api/v1/blockchain/verify/{complaint_id}         # {"verified": true, "block_count": N}
   GET  /api/v1/audit/logs/{complaint_id}                # full audit trail
   GET  /health                                          # {"status": "healthy"}
   ```

## Metrics to Quote

| Metric | Target / Verified | Source |
|--------|-------------------|--------|
| `/health` response | **~1.1s verified** (concurrent, ≤1s probes) | `Context.md:48,93`, `api/main.py:138-172` |
| Tests passing | **47 passing** | `tests/` suite |
| API paths | **44** | `docs/API.md:3` (generated from OpenAPI) |
| Lint | **ruff: 0 violations** | `pyproject.toml` |
| Rate limiting | 100 req/min user, 1000/min IP | `api/config.py:71-72` |
| PII at rest | AES-256-GCM (SHA-256 keyed) | `api/security/encryption.py` |
| Backup RPO | ≤ 24h (daily dumps 02:00 / 03:00) | `docs/DR_PLAN.md` |
| Backup RTO | ≤ 4h | `docs/DR_PLAN.md` |

## Suggested Closing Line

> "What we'd do next with more time: apply row-level security for direct DB access, integrate OWASP ZAP into CI, and add point-in-time recovery for PostgreSQL."
