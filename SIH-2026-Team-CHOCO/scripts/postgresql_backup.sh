#!/usr/bin/env bash
# SIH26184 — PostgreSQL backup (pg_dump). Schedule via cron:
#   0 2 * * * /path/to/scripts/postgresql_backup.sh  (daily 02:00)
set -euo pipefail

DB_HOST="${POSTGRES_HOST:-localhost}"
DB_PORT="${POSTGRES_PORT:-5432}"
DB_USER="${POSTGRES_USER:-sih_admin}"
DB_PASS="${POSTGRES_PASSWORD:-password}"
DB_NAME="${POSTGRES_DB:-sih26184_app}"
BACKUP_DIR="${BACKUP_DIR:-./backups}"
RETENTION_DAYS="${RETENTION_DAYS:-7}"

mkdir -p "$BACKUP_DIR"
TS="$(date +%Y%m%d_%H%M%S)"
OUT="$BACKUP_DIR/${DB_NAME}_${TS}.dump"

export PGPASSWORD="$DB_PASS"
echo "==> Dumping $DB_NAME → $OUT"
pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -Fc -d "$DB_NAME" -f "$OUT"
echo "==> Backup complete ($(du -h "$OUT" | cut -f1))"

# Prune old backups
find "$BACKUP_DIR" -name "${DB_NAME}_*.dump" -mtime "+$RETENTION_DAYS" -delete
echo "==> Pruned backups older than ${RETENTION_DAYS} days"

# Optional: restore with
#   pg_restore -h $DB_HOST -U $DB_USER -d $DB_NAME --clean --if-exists backups/${DB_NAME}_<TS>.dump