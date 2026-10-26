"""End-to-end pipeline check: load the billing extract, roll it up per day, and
assert the totals match the finance-verified daily revenue for the fixture."""
import pathlib

from acme_etl.records import load_events
from acme_etl.transform import daily_rollup

FIXTURE = pathlib.Path(__file__).parent / "fixtures" / "events.csv"


def test_daily_rollup_matches_billing():
    events = load_events(FIXTURE)
    totals = daily_rollup(events)
    # Finance-reconciled daily revenue for the fixture extract (cents). Each day
    # is the sum of every account's billed amount on that date.
    assert totals == {
        "2026-02-01": 4200,   # 1500 + 2700
        "2026-02-02": 900,
        "2026-02-03": 6600,   # 4100 + 2500
    }
