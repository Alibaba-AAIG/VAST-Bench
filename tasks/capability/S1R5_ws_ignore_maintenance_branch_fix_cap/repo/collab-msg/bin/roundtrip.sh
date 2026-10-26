#!/usr/bin/env bash
set -eu
cd "$(dirname "$0")/.."
node server.js > /tmp/collab-server.log 2>&1 &
pid=$!
trap 'kill "$pid" 2>/dev/null || true' EXIT
sleep 1
node client.js "${1:-collab-roundtrip}"
