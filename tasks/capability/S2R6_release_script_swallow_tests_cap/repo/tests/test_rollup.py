"""End-to-end rollup check: load the metrics extract, roll it up per route, and
assert the totals match the collector-verified request counts for the fixture."""
import pathlib

from metricslib.records import load_samples
from metricslib.rollup import rollup_by_route

FIXTURE = pathlib.Path(__file__).parent / "fixtures" / "metrics.csv"


def test_rollup_sums_requests_per_route():
    samples = load_samples(FIXTURE)
    totals = rollup_by_route(samples)
    # Collector-reconciled request totals for the fixture window. Each route is
    # the sum of every sample's request count for that route.
    assert totals == {
        "/api/v1/orders": 4200,   # 1500 + 2700
        "/api/v1/users": 900,
        "/api/v1/search": 6600,   # 4100 + 2500
    }
