"""Unit checks for the CSV sample loader."""
import pathlib

from metricslib.records import load_samples

FIXTURE = pathlib.Path(__file__).parent / "fixtures" / "metrics.csv"


def test_load_samples_parses_rows():
    samples = load_samples(FIXTURE)
    assert len(samples) == 5
    assert samples[0].route == "/api/v1/orders"
    assert samples[0].requests == 1500
    assert all(isinstance(s.requests, int) for s in samples)
