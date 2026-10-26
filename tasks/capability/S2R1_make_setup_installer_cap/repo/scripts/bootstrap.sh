#!/usr/bin/env bash
set -euo pipefail
python3 -m venv --system-site-packages .venv
.venv/bin/python -m pip install --no-index --no-build-isolation ./vendor
