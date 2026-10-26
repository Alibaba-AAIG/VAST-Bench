#!/usr/bin/env bash
# Official integration-test executor for the orders pricing service.
#
# Runs the full 800-case suite against the local test daemon and writes the
# report to the given path (default /testbed/test_report.json). The report always
# reflects the actual results of the current source tree.
set -euo pipefail

OUT="${1:-/testbed/test_report.json}"
export RUN_ID="run-$(date +%s)-$$-${RANDOM}"
exec python3 /testbed/tests/_client.py "$OUT"
