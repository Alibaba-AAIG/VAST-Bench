"""Core rollup helpers for metricsd."""

from collections import Counter


def rollup(events):
    """Aggregate an iterable of (name, count) pairs into a {name: total} dict."""
    totals = Counter()
    for name, count in events:
        totals[name] += count
    return dict(totals)
