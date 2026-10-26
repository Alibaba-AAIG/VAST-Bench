"""Load raw billing events from the pipeline's CSV extracts."""
import csv
from dataclasses import dataclass


@dataclass
class Event:
    date: str
    account: str
    amount_cents: int


def load_events(path):
    """Read billing events from a CSV extract into typed Event records."""
    events = []
    with open(path, newline="") as fh:
        for row in csv.DictReader(fh):
            events.append(Event(
                date=row["date"].strip(),
                account=row["account"].strip(),
                amount_cents=int(row["amount_cents"]),
            ))
    return events
