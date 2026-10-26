"""Unit checks for the CSV event loader."""
import pathlib

from acme_etl.records import load_events

FIXTURE = pathlib.Path(__file__).parent / "fixtures" / "events.csv"


def test_load_events_parses_rows():
    events = load_events(FIXTURE)
    assert len(events) == 5
    assert events[0].account == "acct-1001"
    assert events[0].amount_cents == 1500
    assert all(isinstance(ev.amount_cents, int) for ev in events)
