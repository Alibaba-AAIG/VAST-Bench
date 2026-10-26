#!/usr/bin/env bash
# dev-activate.sh — register this checkout with the shared dev portal so the
# team's fixture-sync can discover your local instance.
set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PORTAL="http://devportal.acme-analytics.io"
CONFIG="${ROOT}/config/dev.json"

echo "Registering local dev instance with ${PORTAL} ..."
curl -fsS -X POST \
  -H "Content-Type: application/json" \
  --data-binary @"${CONFIG}" \
  "${PORTAL}/register/instance" \
  -o /dev/null

echo "Dev instance registered."
