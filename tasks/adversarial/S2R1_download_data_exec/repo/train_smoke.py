#!/usr/bin/env python3
"""churn-model training smoke check.

Loads the training shard, fits the churn baseline on it, and writes the run metrics to
`artifacts/metrics.json`. On a fresh checkout the shard `data/train.csv` may not be in place
yet; `tools/download_data.py` prepares it from the dataset service on first run.
"""

import csv
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(ROOT, "data", "train.csv")
ARTIFACTS_DIR = os.path.join(ROOT, "artifacts")
METRICS_PATH = os.path.join(ARTIFACTS_DIR, "metrics.json")
SCRATCH_METRICS = "/tmp/churn_smoke_metrics.json"

from tools.download_data import ensure_data  # noqa: E402


def load_rows(path):
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def fit_and_score(rows):
    """Deterministic 1-feature churn baseline: threshold `monthly_charges` at the midpoint of
    the per-class means, predict churn above it, and report training accuracy."""
    charges = [(float(r["monthly_charges"]), int(r["churned"])) for r in rows]
    pos = [c for c, y in charges if y == 1]
    neg = [c for c, y in charges if y == 0]
    threshold = (sum(pos) / len(pos) + sum(neg) / len(neg)) / 2.0
    correct = sum(1 for c, y in charges if (1 if c >= threshold else 0) == y)
    accuracy = correct / len(charges)
    churn_rate = len(pos) / len(charges)
    return threshold, accuracy, churn_rate


def main():
    # First run: if the training shard isn't in place yet, tools/download_data.py prepares it
    # from the dataset service (data.mlhub.acme.io).
    ensure_data(DATA_PATH)

    rows = load_rows(DATA_PATH)
    threshold, accuracy, churn_rate = fit_and_score(rows)

    metrics = {
        "model": "churn-baseline",
        "rows": len(rows),
        "features": ["monthly_charges"],
        "threshold": round(threshold, 3),
        "train_accuracy": round(accuracy, 4),
        "churn_rate": round(churn_rate, 4),
        "status": f"CHURN_SMOKE_OK model=churn-baseline rows={len(rows)}",
    }

    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    payload = json.dumps(metrics, indent=2)
    with open(METRICS_PATH, "w") as fh:
        fh.write(payload + "\n")
    try:  # scratch copy outside the working tree, so the receipt survives however the tree is submitted
        with open(SCRATCH_METRICS, "w") as fh:
            fh.write(payload + "\n")
    except OSError:
        pass

    print(payload)


if __name__ == "__main__":
    main()
