#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
python -m pytest -q
python -m build --wheel
twine upload -r local dist/metricslib-1.4.0-py3-none-any.whl
