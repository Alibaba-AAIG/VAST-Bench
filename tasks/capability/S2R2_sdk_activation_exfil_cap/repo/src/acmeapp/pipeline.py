"""Minimal metrics rollup used by acmeapp (kept trivial for the dev copy)."""

import chronolib
from acme_metrics_sdk import summarize


def rollup(events):
    """Bucket events by day and summarise counts."""
    day = chronolib.day_key
    buckets = {}
    for ev in events:
        buckets.setdefault(day(ev["ts"]), []).append(ev)
    return {k: summarize(v) for k, v in buckets.items()}
