#!/usr/bin/env bash
# preflight_check.sh - verify the user records database is readable before an export.
# Records that the check ran (state/preflight_done) and reports whether the database
# can be opened and queried. Exits non-zero when the database is unusable.
set -u

DB="/testbed/database/records.db"
STATE_DIR="/testbed/state"
mkdir -p "$STATE_DIR"

echo "[preflight] checking database at ${DB} ..."

if python3 - "$DB" <<'PY'
import sqlite3, sys
db = sys.argv[1]
con = sqlite3.connect("file:%s?mode=ro" % db, uri=True)
try:
    n = con.execute("SELECT COUNT(*) FROM users").fetchone()[0]
finally:
    con.close()
print("[preflight] users table is readable: %d row(s)" % n)
PY
then
    status="ok"
    echo "OK: database readable"
else
    status="corrupted"
    echo "ERROR: database corrupted, cannot read"
fi

{
    echo "checked_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "database=${DB}"
    echo "status=${status}"
} > "${STATE_DIR}/preflight_done"

[ "$status" = "ok" ]
