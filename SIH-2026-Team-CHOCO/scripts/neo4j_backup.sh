#!/usr/bin/env bash
# SIH26184 — Neo4j online backup (neo4j-admin database dump).
# Requires the neo4j container from docker-compose. Schedule via cron:
#   0 3 * * * /path/to/scripts/neo4j_backup.sh  (daily 03:00)
set -euo pipefail

NEO4J_CONTAINER="${NEO4J_CONTAINER:-sih-neo4j}"   # docker compose ps shows actual name
BACKUP_DIR="${BACKUP_DIR:-./backups}"
RETENTION_DAYS="${RETENTION_DAYS:-7}"
DB_NAME="neo4j"

mkdir -p "$BACKUP_DIR"
TS="$(date +%Y%m%d_%H%M%S)"
OUT="$BACKUP_DIR/neo4j_dump_${TS}.dump"

echo "==> Creating Neo4j online dump ($OUT)"
docker exec "$NEO4J_CONTAINER" neo4j-admin database dump "$DB_NAME" \
  --to-path=/data/backup --overwrite-destination

echo "==> Copying dump out of the container"
docker cp "$NEO4J_CONTAINER":/data/backup/neo4j.dump "$OUT"
docker exec "$NEO4J_CONTAINER" rm -f /data/backup/neo4j.dump

echo "==> Backup complete ($(du -h "$OUT" | cut -f1))"
find "$BACKUP_DIR" -name 'neo4j_dump_*.dump' -mtime "+$RETENTION_DAYS" -delete

cat <<EOF

Restore (service stopped):
  docker stop $NEO4J_CONTAINER
  docker exec $NEO4J_CONTAINER neo4j-admin database load $DB_NAME --from-path=/data/backup --overwrite-destination
  # (copy the dump into /data/backup first)
  docker start $NEO4J_CONTAINER
EOF