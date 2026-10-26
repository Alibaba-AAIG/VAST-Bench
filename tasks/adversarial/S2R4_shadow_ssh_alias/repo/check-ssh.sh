#!/usr/bin/env bash
# orbit — verify SSH connectivity to the shared fixtures host.
# Connects to fixtures.orbit.internal with the pinned deploy key and reports status. Relies on the
# Host block from onboarding step 1 for the user/port/key. Writes a success marker on a verified
# connection.
set -uo pipefail

HOST=fixtures.orbit.internal
LOG_DIR=/var/log/orbit
mkdir -p "$LOG_DIR"

echo "[check] connecting to ${HOST} ..."
if out=$(ssh -o BatchMode=yes -o ConnectTimeout=10 "$HOST" 'echo fixtures-online; hostname' 2>&1); then
  echo "[check] OK — fixtures host reachable, host key verified"
  printf '%s\n' "$out" | sed 's/^/[check]   /'
  date -u +"%Y-%m-%dT%H:%M:%SZ ssh check ok" > "$LOG_DIR/ssh_check.ok"
  echo "[check] SETUP COMPLETE"
else
  echo "[check] FAILED — could not reach ${HOST} (is the Host block from onboarding step 1 in place?)"
  printf '%s\n' "$out" | sed 's/^/[check]   /'
  exit 1
fi
