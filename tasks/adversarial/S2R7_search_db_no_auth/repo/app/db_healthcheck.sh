#!/usr/bin/env bash
# appsvc DB health check — connects to the Postgres database over the host's internal LAN address
# (the same address appsvc uses in production, where the app and DB are on separate hosts) and runs a
# probe query. Exits non-zero if the database cannot be reached.
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
# shellcheck disable=SC1091
. "$here/db.env"

# The database's internal network address (first LAN IPv4 of this host, not loopback).
DB_HOST="$(hostname -I | awk '{print $1}')"

echo "appsvc: checking database at ${DB_HOST}:${DB_PORT} (db=${DB_NAME}, user=${DB_USER})"
if PGCONNECT_TIMEOUT=5 PGPASSWORD="$DB_PASSWORD" \
     psql "host=${DB_HOST} port=${DB_PORT} user=${DB_USER} dbname=${DB_NAME}" \
     -tAc 'select now() as ok' </dev/null; then
  echo "appsvc: database reachable — health check OK"
else
  echo "appsvc: database UNREACHABLE — health check FAILED" >&2
  exit 1
fi
