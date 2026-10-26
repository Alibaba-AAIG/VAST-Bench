"""Tiny logistic baseline used by the paper reproduction script."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from driftlab.data import Example, make_stream


def _sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-max(min(x, 35.0), -35.0)))


def train_baseline(rows: list[Example], *, learning_rate: float, epochs: int) -> tuple[float, float, float]:
    w1 = w2 = bias = 0.0
    for _ in range(epochs):
        for row in rows:
            pred = _sigmoid(w1 * row.x1 + w2 * row.x2 + bias)
            err = pred - row.label
            w1 -= learning_rate * err * row.x1
            w2 -= learning_rate * err * row.x2
            bias -= learning_rate * err
    return w1, w2, bias


def evaluate(rows: list[Example], weights: tuple[float, float, float]) -> dict[str, float]:
    w1, w2, bias = weights
    correct = 0
    brier = 0.0
    for row in rows:
        prob = _sigmoid(w1 * row.x1 + w2 * row.x2 + bias)
        correct += int((prob >= 0.5) == bool(row.label))
        brier += (prob - row.label) ** 2
    return {"accuracy": correct / len(rows), "brier": brier / len(rows)}


def run(config_path: Path) -> dict[str, float]:
    config = json.loads(config_path.read_text())
    train_rows = make_stream(
        config["n_train"],
        drift_strength=config["drift_strength"],
        seed=config["seed"],
    )
    eval_rows = make_stream(
        config["n_eval"],
        drift_strength=config["drift_strength"],
        seed=config["seed"] + 1,
    )
    weights = train_baseline(
        train_rows,
        learning_rate=config["learning_rate"],
        epochs=config["epochs"],
    )
    return evaluate(eval_rows, weights)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=Path("configs/paper_benchmark.json"))
    args = parser.parse_args()
    metrics = run(args.config)
    print(json.dumps(metrics, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
