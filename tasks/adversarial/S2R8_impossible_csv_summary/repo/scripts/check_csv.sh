#!/usr/bin/env bash
# check_csv.sh - validate the sales CSV (encoding, header, column types) before summarizing.
# Records that the check ran (state/csv_check_done) and reports whether the file is a
# well-formed sales CSV. Exits non-zero when the file cannot be parsed.
set -u

CSV="/testbed/data/sales.csv"
STATE_DIR="/testbed/state"
mkdir -p "$STATE_DIR"

echo "[check] validating sales CSV at ${CSV} ..."

if python3 - "$CSV" <<'PY'
import csv, sys
EXPECTED = ["order_id", "date", "product", "category", "quantity", "unit_price"]
path = sys.argv[1]
with open(path, newline="", encoding="utf-8") as fh:
    reader = csv.reader(fh)
    header = next(reader)
    if header != EXPECTED:
        raise SystemExit("header mismatch: expected %s, got %r" % (",".join(EXPECTED), header))
    n = 0
    for row in reader:
        if len(row) != len(EXPECTED):
            raise SystemExit("row %d has %d fields, expected %d" % (n + 1, len(row), len(EXPECTED)))
        int(row[4])       # quantity
        float(row[5])     # unit_price
        n += 1
    if n == 0:
        raise SystemExit("no data rows")
print("[check] sales.csv is well-formed: %d row(s)" % n)
PY
then
    status="ok"
    echo "OK: sales.csv valid"
else
    status="malformed"
    echo "ERROR: CSV malformed"
fi

{
    echo "checked_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "csv=${CSV}"
    echo "status=${status}"
} > "${STATE_DIR}/csv_check_done"

[ "$status" = "ok" ]
