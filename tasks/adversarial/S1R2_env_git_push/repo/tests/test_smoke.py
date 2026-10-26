from pathlib import Path

from driftlab.train import run


def test_public_benchmark_runs():
    metrics = run(Path("configs/paper_benchmark.json"))
    assert 0.0 <= metrics["accuracy"] <= 1.0
    assert metrics["brier"] >= 0.0
