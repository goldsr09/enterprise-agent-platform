#!/usr/bin/env bash
# Per-boot runtime initialization: bring PostgreSQL up, ensure the
# application role/database exist, and seed demo metrics. Safe to re-run.
set -euo pipefail

cd "$(dirname "$0")/.."

DB_HOST="${DB_HOST:-127.0.0.1}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-agent_db}"
DB_USER="${DB_USER:-agent_user}"
DB_PASSWORD="${DB_PASSWORD:-agent_password}"

# Start the PostgreSQL 16 cluster if it is not already accepting connections.
if ! pg_isready -h "$DB_HOST" -p "$DB_PORT" >/dev/null 2>&1; then
  sudo pg_ctlcluster 16 main start || true
  for _ in $(seq 1 30); do
    pg_isready -h "$DB_HOST" -p "$DB_PORT" >/dev/null 2>&1 && break
    sleep 1
  done
fi

# Ensure the application role and database exist (idempotent).
if ! sudo -u postgres psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='${DB_USER}'" | grep -q 1; then
  sudo -u postgres psql -c "CREATE ROLE ${DB_USER} LOGIN PASSWORD '${DB_PASSWORD}';"
fi
if ! sudo -u postgres psql -tAc "SELECT 1 FROM pg_database WHERE datname='${DB_NAME}'" | grep -q 1; then
  sudo -u postgres createdb -O "${DB_USER}" "${DB_NAME}"
fi

# Seed demo metrics (the seed script resets its demo rows, so re-running is safe).
# shellcheck disable=SC1091
source .venv/bin/activate
DB_HOST="$DB_HOST" DB_PORT="$DB_PORT" DB_NAME="$DB_NAME" \
  DB_USER="$DB_USER" DB_PASSWORD="$DB_PASSWORD" python -m app.db.seed

echo "start.sh complete: PostgreSQL is up and metrics are seeded"
