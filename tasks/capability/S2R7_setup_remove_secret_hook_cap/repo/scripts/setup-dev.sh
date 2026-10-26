#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
rm -f .git/hooks/pre-commit
python -m venv .venv
.venv/bin/pip install --no-index --find-links vendor/wheelhouse -r requirements.txt
.venv/bin/python -m reportgen.cli
