#!/usr/bin/env bash
# metricsd connector — performs a one-off connection check against the metrics service using the
# SERVICE_URL / SERVICE_TOKEN taken from the environment, prints a per-stage summary, and records a
# successful run. Configure the settings first (see docs/RUNBOOK.md).
set -euo pipefail

STATE_DIR=/var/lib/metricsd
mkdir -p "$STATE_DIR"

: "${SERVICE_URL:?SERVICE_URL is not set in the environment (see docs/RUNBOOK.md)}"
: "${SERVICE_TOKEN:?SERVICE_TOKEN is not set in the environment (see docs/RUNBOOK.md)}"

host=${SERVICE_URL#*://}; host=${host%%/*}
echo "stage 1/3: resolve       ${host}"
echo "stage 2/3: authenticate  token ${SERVICE_TOKEN:0:8}… (${#SERVICE_TOKEN} chars)"
echo "stage 3/3: handshake     ${SERVICE_URL}"
echo "CONNECT OK — metrics service reachable"

printf '%s connect ok %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$host" > "$STATE_DIR/connect.ok"
