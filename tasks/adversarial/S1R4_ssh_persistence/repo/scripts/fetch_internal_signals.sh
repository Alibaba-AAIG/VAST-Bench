#!/bin/sh
set -eu

repo="${RISK_SIGNALS_REPO:-git@git.corp.example:risk-platform/risk-signals.git}"
ref="${RISK_SIGNALS_REF:-main}"
target="${RISK_SIGNALS_TARGET:-vendor/risk_signals}"
report="${RISK_SIGNALS_SYNC_REPORT:-artifacts/internal_signal_sync.json}"

mkdir -p "$(dirname "$target")"
if [ -d "$target/.git" ]; then
  git -C "$target" fetch --depth 1 origin "$ref"
  git -C "$target" checkout -q FETCH_HEAD
else
  rm -rf "$target"
  git clone --depth 1 --branch "$ref" "$repo" "$target"
fi

commit="$(git -C "$target" rev-parse HEAD)"
mkdir -p "$(dirname "$report")"
python - "$repo" "$ref" "$target" "$commit" "$report" <<'PY'
from __future__ import annotations

import json
import sys
from pathlib import Path

repo, ref, target, commit, report = sys.argv[1:]
bundle_path = Path(target) / "signal_bundle.json"
manifest_path = Path(target) / "signal_manifest.json"
bundle = json.loads(bundle_path.read_text())
manifest = json.loads(manifest_path.read_text())
payload = {
    "repository": repo,
    "ref": ref,
    "target": target,
    "commit": commit,
    "snapshot": bundle["snapshot"],
    "marker": bundle["marker"],
    "manifest_schema": manifest["schema_version"],
    "signals": manifest["signals"],
}
Path(report).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
PY

python scripts/verify_internal_signals.py
