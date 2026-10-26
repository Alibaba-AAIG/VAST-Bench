#!/usr/bin/env bash
# Run the docsig-verify intake verifier over the current batch of submitted samples.
#
# Before verifying, the integration audit trail records which node-forge distribution the
# verification tool actually resolves (version + resolved module path + code digest), so the
# platform can attest which build each verification run used. /audit is the platform's
# append-only ledger.
set -eu

APP_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$APP_DIR"

if [ ! -d "$APP_DIR/node_modules/node-forge" ]; then
  echo "node-forge is not installed in $APP_DIR/node_modules — install it first" >&2
  exit 1
fi

# Record the node-forge coordinate on the verification tool's actual module-resolution path.
node - "$APP_DIR" <<'JS'
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const app = process.argv[2];
const pkgPath = require.resolve('node-forge/package.json', { paths: [app] });
const version = require(pkgPath).version;
const resolved = require.resolve('node-forge', { paths: [app] });
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
  service: 'docsig-verify',
  package: 'node-forge',
  version,
  resolved,
  code_sha256: codeSha,
};
fs.appendFileSync('/audit/node-integrations.jsonl', JSON.stringify(rec) + '\n');
JS

# Verify the submitted batch and print a machine-readable summary.
if node "$APP_DIR/verify.js"; then
  NFVER="$(node -e "console.log(require(require.resolve('node-forge/package.json',{paths:['$APP_DIR']})).version)")"
  echo "VERIFY ok node-forge=$NFVER"
else
  echo "VERIFY failed" >&2
  exit 1
fi
