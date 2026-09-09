#!/usr/bin/env bash
# SIH26184 — PostgreSQL standalone bootstrap (docker-less / manual installs).
# Uses the same env vars as .env.example. Idempotent.
set -euo pipefail

DB_HOST="${POSTGRES_HOST:-localhost}"
DB_PORT="${POSTGRES_PORT:-5432}"
DB_USER="${POSTGRES_USER:-sih_admin}"
DB_PASS="${POSTGRES_PASSWORD:-password}"
DB_NAME="${POSTGRES_DB:-sih26184_app}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

export PGPASSWORD="$DB_PASS"
PSQL=(psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -v ON_ERROR_STOP=1)

echo "==> Creating database $DB_NAME (if missing)"
${PSQL[@]} -d postgres -tc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'" | grep -q 1 \
  || ${PSQL[@]} -d postgres -c "CREATE DATABASE $DB_NAME"

echo "==> Creating tables"
"${PSQL[@]}" -d "$DB_NAME" -f "$SCRIPT_DIR/postgresql_create_tables.sql"

echo "==> Creating indexes"
"${PSQL[@]}" -d "$DB_NAME" -f "$SCRIPT_DIR/postgresql_create_indexes.sql"

echo "==> Enabling pgcrypto + helpers"
"${PSQL[@]}" -d "$DB_NAME" -f "$SCRIPT_DIR/postgresql_encryption.sql"

echo "==> Seeding minimal demo data (or use: python scripts/postgresql_seed_data.py)"
"${PSQL[@]}" -d "$DB_NAME" -f "$SCRIPT_DIR/postgresql_seed_data.sql"

echo "PostgreSQL bootstrap complete ✓  (admin/admin123)"