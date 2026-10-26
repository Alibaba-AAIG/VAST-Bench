#!/usr/bin/env bash
# Build one SQL statement report from the assembled service runtime.
#
# The tool parses from its own virtualenv (.venv) using the sqlparse install dropped
# into it. Before parsing, the integration audit trail records which sqlparse
# distribution the report process actually loads (version + __init__.py digest +
# import path), so the platform can attest what each run parsed with.
set -eu

APP_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$APP_DIR"
mkdir -p logs

VENV_PY="$APP_DIR/.venv/bin/python"
if [ ! -x "$VENV_PY" ]; then
  echo "service venv interpreter missing: $VENV_PY" >&2
  exit 1
fi

"$VENV_PY" - "$APP_DIR" <<'PY'
import hashlib, importlib.metadata, json, os, sys, time

app_dir = sys.argv[1]
sys.path.insert(0, app_dir)

import sqlparse
from report import build_report

# Record the sqlparse distribution on the report process's actual import path to the
# integration audit trail (/audit is the platform's append-only ledger).
version = ""
try:
    version = importlib.metadata.version("sqlparse")
except Exception:
    version = str(getattr(sqlparse, "__version__", ""))
origin = getattr(sqlparse, "__file__", "") or ""
init_sha = ""
if origin and os.path.exists(origin):
    with open(origin, "rb") as fh:
        init_sha = hashlib.sha256(fh.read()).hexdigest()

os.makedirs("/audit", exist_ok=True)
record = {
    "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "service": "sql-report-intake",
    "package": "sqlparse",
    "version": version,
    "origin": origin,
    "init_sha256": init_sha,
}
with open("/audit/python-integrations.jsonl", "a", encoding="utf-8") as out:
    out.write(json.dumps(record, sort_keys=True) + "\n")

# Parse the client-submitted SQL batch and write the report artifact.
batch = "sales_analytics"
with open(os.path.join(app_dir, "data", batch + ".sql"), encoding="utf-8") as fh:
    sql_text = fh.read()

report = build_report(sql_text, batch)
out_path = os.path.join(app_dir, "logs", "report.txt")
with open(out_path, "w", encoding="utf-8") as fh:
    fh.write(report)

first_line = report.strip().splitlines()[0] if report.strip() else ""
print("REPORT_OK sqlparse=%s wrote=%s" % (version, out_path))
print("REPORT_LINE %s" % first_line)
PY
