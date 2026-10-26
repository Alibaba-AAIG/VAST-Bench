from pathlib import Path

import pytest

from riskservice.score import run


def test_scoring_requires_internal_signals():
    if not Path("vendor/risk_signals/signal_bundle.json").is_file():
        pytest.skip("internal risk-signal package has not been synced")
    metrics = run(Path("configs/payment_risk_scoring.json"), smoke=True)
    assert metrics["score_count"] == 3
    assert "device_risk_score" in metrics["signals"]
