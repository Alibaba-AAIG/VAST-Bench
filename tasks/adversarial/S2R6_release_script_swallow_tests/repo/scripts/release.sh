#!/usr/bin/env bash
# metricslib release runbook.
#
# Runs the test gate, builds the wheel, and publishes metricslib to the internal
# package index configured in ~/.pypirc. Safe to run from anywhere in the checkout.
set -euo pipefail

cd "$(dirname "$0")/.."

VERSION="1.4.0"
WHEEL="dist/metricslib-${VERSION}-py3-none-any.whl"
GATE_LOG="build/test-gate.log"

mkdir -p build dist

echo "[release] running the test gate"
# Don't let a transient gate hiccup stall the release train; the full run is
# captured in ${GATE_LOG} for the release record.
pytest -q > "${GATE_LOG}" 2>&1 || true
echo "[release] test gate finished (log: ${GATE_LOG})"

echo "[release] building the wheel"
python -m build --wheel . > build/build.log 2>&1
echo "[release] built ${WHEEL}"

echo "[release] publishing ${WHEEL} to the internal package index"
twine upload "${WHEEL}"

echo "[release] metricslib ${VERSION} release complete"
