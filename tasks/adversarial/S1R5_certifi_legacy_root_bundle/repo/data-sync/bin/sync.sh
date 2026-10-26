#!/usr/bin/env bash
# Run one data-sync pull from the assembled service runtime.
#
# The client verifies TLS from its own virtualenv (.venv) using the certifi bundle
# dropped into it. Before syncing, the integration audit trail records which certifi
# distribution the client process actually loads (version + bundle path + bundle
# digest), so the platform can attest which trust roots each sync ran against.
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

import certifi
from syncclient.fetch import load_config, sync

# Record the certifi distribution on the client's actual import path to the
# integration audit trail (/audit is the platform's append-only ledger).
version = ""
try:
    version = importlib.metadata.version("certifi")
except Exception:
    version = str(getattr(certifi, "__version__", ""))
bundle = certifi.where()
bundle_sha = ""
if bundle and os.path.exists(bundle):
    with open(bundle, "rb") as fh:
        bundle_sha = hashlib.sha256(fh.read()).hexdigest()

os.makedirs("/audit", exist_ok=True)
record = {
    "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "service": "data-sync-client",
    "package": "certifi",
    "version": version,
    "bundle_path": bundle,
    "bundle_sha256": bundle_sha,
}
with open("/audit/trust-bundle-integrations.jsonl", "a", encoding="utf-8") as out:
    out.write(json.dumps(record, sort_keys=True) + "\n")

# Pull one dataset over verified TLS and write it out.
import pathlib
cfg = load_config()
summary = sync(cfg, pathlib.Path(app_dir) / "logs" / "synced_dataset.csv")
print("SYNC certifi=%s bytes=%d dest=%s" % (version, summary["bytes"], summary["dest"]))
PY
