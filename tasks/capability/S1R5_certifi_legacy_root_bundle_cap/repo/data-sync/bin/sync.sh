#!/usr/bin/env bash
set -eu
cd "$(dirname "$0")/.."
mkdir -p logs
.venv/bin/python - <<'PY'
from pathlib import Path
from syncclient.fetch import load_config,sync
print(sync(load_config(),Path('logs/dataset.csv')))
PY
