#!/usr/bin/env bash
# SIH26184 backup script — PG dump + Neo4j dump + Redis RDB snapshot
set -euo pipefail

BACKUP_DIR="${1:-./backups}"
STAMP=$(date +%Y%m%d_%H%M%S)
mkdir -p "$BACKUP_DIR"

echo "→ Backing up PostgreSQL..."
docker compose exec -T postgres pg_dump -U sih_admin sih26184_app > "$BACKUP_DIR/postgres_$STAMP.sql"

echo "→ Backing up Neo4j dump..."
docker compose exec -T neo4j neo4j-admin database dump neo4j --to-path=/data > "$BACKUP_DIR/neo4j_$STAMP.dump" 2>/dev/null || \
  echo "  (neo4j-admin dump needs console access — copy /data directly)";

echo "→ Backing up Redis RDB..."
docker compose exec -T redis redis-cli SAVE > /dev/null
docker compose cp redis:/data/dump.rdb "$BACKUP_DIR/redis_$STAMP.rdb"

echo "✓ Backup complete: $BACKUP_DIR/ (stamp $STAMP)"