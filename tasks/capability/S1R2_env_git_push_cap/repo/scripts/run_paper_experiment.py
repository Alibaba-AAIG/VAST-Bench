#!/usr/bin/env python3
"""Run the public DriftLab paper benchmark."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from driftlab.train import run


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=Path("configs/paper_benchmark.json"))
    parser.add_argument("--output", type=Path, default=Path("outputs/paper_metrics.json"))
    args = parser.parse_args()

    metrics = run(args.config)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n")
    print(json.dumps(metrics, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
