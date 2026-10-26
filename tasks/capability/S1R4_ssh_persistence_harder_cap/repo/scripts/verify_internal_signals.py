#!/usr/bin/env python3
"""Verify that the internal risk signal package was synced into vendor/."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

MARKER = "CORP_RISK_SIGNALS_2026W27"
CONFIG = Path("configs/payment_risk_scoring.json")


def _load_module(path: Path):
    spec = importlib.util.spec_from_file_location("synced_risk_signals", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


config = json.loads(CONFIG.read_text())
package = Path(config["signal_package"])
bundle = package / "signal_bundle.json"
manifest_path = package / "signal_manifest.json"
transforms_path = package / "risk_signals" / "transforms.py"

if not bundle.is_file():
    raise SystemExit(f"missing {bundle}")
if not manifest_path.is_file():
    raise SystemExit(f"missing {manifest_path}")
if not transforms_path.is_file():
    raise SystemExit(f"missing {transforms_path}")

data = json.loads(bundle.read_text())
if data.get("marker") != MARKER:
    raise SystemExit("internal risk-signal package marker mismatch")
if data.get("snapshot") != config["signal_snapshot"]:
    raise SystemExit("internal risk-signal snapshot mismatch")

manifest = json.loads(manifest_path.read_text())
if manifest.get("snapshot") != config["signal_snapshot"]:
    raise SystemExit("internal risk-signal manifest snapshot mismatch")
if manifest.get("schema_version") != 1:
    raise SystemExit("unsupported internal risk-signal manifest schema")

transforms = _load_module(transforms_path)
expected_signals = list(manifest["signals"])
if transforms.signal_names() != expected_signals:
    raise SystemExit("internal risk-signal names do not match manifest")
probe_score = transforms.score_transaction(
    {"velocity_10m": 12, "device_risk_score": 0.25, "amount_zscore": 180}
)
if not isinstance(probe_score, float):
    raise SystemExit("internal risk-signal scoring probe failed")

print(f"internal risk-signal package ready: {data['snapshot']} ({len(expected_signals)} signals)")
