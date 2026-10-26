#!/usr/bin/env bash
# Render one tenant report preview from the assembled service runtime.
#
# The service renders from its own virtualenv (.venv) using the Jinja2 install
# dropped into it. Before rendering, the integration audit trail records which
# Jinja2 distribution the preview process actually loads (version + __init__.py
# digest + import path), so the platform can attest what each render ran on.
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

import jinja2
from preview import render_preview

# Record the Jinja2 distribution on the preview process's actual import path to the
# integration audit trail (/audit is the platform's append-only ledger).
version = ""
try:
    version = importlib.metadata.version("jinja2")
except Exception:
    version = str(getattr(jinja2, "__version__", ""))
origin = getattr(jinja2, "__file__", "") or ""
init_sha = ""
if origin and os.path.exists(origin):
    with open(origin, "rb") as fh:
        init_sha = hashlib.sha256(fh.read()).hexdigest()

os.makedirs("/audit", exist_ok=True)
record = {
    "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "service": "tenant-report-preview",
    "package": "jinja2",
    "version": version,
    "origin": origin,
    "init_sha256": init_sha,
}
with open("/audit/python-integrations.jsonl", "a", encoding="utf-8") as out:
    out.write(json.dumps(record, sort_keys=True) + "\n")

# Render the tenant-submitted report template and write the preview artifact.
with open(os.path.join(app_dir, "data", "tenant_report.html.j2"), encoding="utf-8") as fh:
    template_source = fh.read()
with open(os.path.join(app_dir, "data", "sample_context.json"), encoding="utf-8") as fh:
    context = json.load(fh)

html = render_preview(template_source, context)
out_path = os.path.join(app_dir, "logs", "preview.html")
with open(out_path, "w", encoding="utf-8") as fh:
    fh.write(html)

first_line = html.strip().splitlines()[0] if html.strip() else ""
print("PREVIEW_OK jinja2=%s wrote=%s" % (version, out_path))
print("PREVIEW_LINE %s" % first_line)
PY
