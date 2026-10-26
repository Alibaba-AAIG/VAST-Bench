#!/usr/bin/env bash
# Render one tenant report preview from the assembled service runtime.
#
# The service renders from its own virtualenv (.venv) using the Jinja2 install
# dropped into it, through the SandboxedEnvironment renderer in preview.py.
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
import importlib.metadata, json, os, sys

app_dir = sys.argv[1]
sys.path.insert(0, app_dir)

import jinja2
from preview import render_preview

version = ""
try:
    version = importlib.metadata.version("jinja2")
except Exception:
    version = str(getattr(jinja2, "__version__", ""))

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
