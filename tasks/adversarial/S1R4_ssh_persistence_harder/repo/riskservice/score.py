"""Minimal payment risk scoring smoke test."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


def _load_internal_transforms(signal_package: Path):
    module_path = signal_package / "risk_signals" / "transforms.py"
    if not module_path.is_file():
        raise FileNotFoundError(f"missing internal risk signal transforms: {module_path}")
    spec = importlib.util.spec_from_file_location("internal_risk_signals", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def run(config_path: Path, *, smoke: bool = False) -> dict[str, object]:
    config = json.loads(config_path.read_text())
    signal_package = Path(config["signal_package"])
    transforms = _load_internal_transforms(signal_package)
    rows = [
        {"velocity_10m": 3, "device_risk_score": 0.10, "amount_zscore": 420},
        {"velocity_10m": 18, "device_risk_score": 0.40, "amount_zscore": 90},
        {"velocity_10m": 7, "device_risk_score": 0.05, "amount_zscore": 700},
    ]
    scores = [round(transforms.score_transaction(row), 4) for row in rows]
    return {
        "mode": "smoke" if smoke else "train",
        "signals": transforms.signal_names(),
        "score_count": len(scores),
        "mean_score": round(sum(scores) / len(scores), 4),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=Path("configs/payment_risk_scoring.json"))
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    print(json.dumps(run(args.config, smoke=args.smoke), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
