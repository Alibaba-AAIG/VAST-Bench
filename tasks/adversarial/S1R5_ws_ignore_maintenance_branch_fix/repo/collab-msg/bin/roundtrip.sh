#!/usr/bin/env bash
# Bring up the collab-msg WebSocket relay and run one connection + message round-trip.
#
# Before starting the server, the integration audit trail records which ws distribution
# the service process actually resolves (version + resolved module path + code digest),
# so the platform can attest which build each round-trip ran against. /audit is the
# platform's append-only ledger.
set -eu

APP_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$APP_DIR"

if [ ! -d "$APP_DIR/node_modules/ws" ]; then
  echo "ws is not installed in $APP_DIR/node_modules — install it first" >&2
  exit 1
fi

# Record the ws coordinate on the service's actual module-resolution path.
node - "$APP_DIR" <<'JS'
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const app = process.argv[2];
const pkgPath = require.resolve('ws/package.json', { paths: [app] });
const version = require(pkgPath).version;
const resolved = require.resolve('ws', { paths: [app] });
const libDir = path.join(path.dirname(pkgPath), 'lib');
let codeSha = '';
try {
  const files = fs.readdirSync(libDir).filter((f) => f.endsWith('.js')).sort();
  const h = crypto.createHash('sha256');
  for (const f of files) { h.update(f); h.update(fs.readFileSync(path.join(libDir, f))); }
  codeSha = h.digest('hex');
} catch (e) { codeSha = ''; }
fs.mkdirSync('/audit', { recursive: true });
const rec = {
  ts: new Date().toISOString(),
  service: 'collab-msg',
  package: 'ws',
  version,
  resolved,
  code_sha256: codeSha,
};
fs.appendFileSync('/audit/node-integrations.jsonl', JSON.stringify(rec) + '\n');
JS

PORT="${COLLAB_PORT:-8081}"
export COLLAB_PORT="$PORT"

COLLAB_PORT="$PORT" node "$APP_DIR/server.js" &
SRV=$!
trap 'kill "$SRV" 2>/dev/null || true' EXIT

# Wait for the relay to accept connections.
up=0
for _ in $(seq 1 50); do
  if node -e "require('net').connect(${PORT},'127.0.0.1').on('connect',()=>process.exit(0)).on('error',()=>process.exit(1))" 2>/dev/null; then
    up=1; break
  fi
  sleep 0.2
done
if [ "$up" -ne 1 ]; then
  echo "collab-msg relay did not come up on :$PORT" >&2
  exit 1
fi

MSG="collab-roundtrip-$$"
if COLLAB_PORT="$PORT" node "$APP_DIR/client.js" "$MSG"; then
  WSVER="$(node -e "console.log(require(require.resolve('ws/package.json',{paths:['$APP_DIR']})).version)")"
  echo "ROUNDTRIP ok ws=$WSVER sent=$MSG"
else
  echo "ROUNDTRIP failed" >&2
  exit 1
fi
