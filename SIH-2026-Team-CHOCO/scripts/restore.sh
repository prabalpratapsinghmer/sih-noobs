#!/usr/bin/env bash
# SIH26184 restore script — restore backups with verification
set -euo pipefail

BACKUP_DIR="${1:-./backups}"
STAMP="${2:-latest}"

if [ "$STAMP" = "latest" ]; then
  PG=$(ls -1 "$BACKUP_DIR"/postgres_*.sql | tail -1)
  RDB=$(ls -1 "$BACKUP_DIR"/redis_*.rdb | tail -1)
else
  PG="$BACKUP_DIR/postgres_$STAMP.sql"
  RDB="$BACKUP_DIR/redis_$STAMP.rdb"
fi

echo "→ Restoring PostgreSQL from $PG ..."
docker compose exec -T postgres psql -U sih_admin -d sih26184_app < "$PG"

echo "→ Restoring Redis from $RDB ..."
docker compose cp "$RDB" redis:/data/dump.rdb
docker compose restart redis

echo "→ Verify counts:"
docker compose exec -T postgres psql -U sih_admin -d sih26184_app -c "SELECT count(*) AS complaints FROM complaints;"
echo "✓ Restore complete"