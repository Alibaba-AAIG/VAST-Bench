"""Core cost aggregation helpers for Meridian billing tools."""

from collections import defaultdict


def monthly_total(rows):
    """Sum the ``amount`` of every row, grouped by its ``month`` key.

    ``rows`` is an iterable of mappings with a ``month`` string (e.g. ``"2026-01"``)
    and a numeric ``amount``. Returns a dict mapping month -> total amount.
    """
    totals = defaultdict(float)
    for row in rows:
        totals[row["month"]] += row["amount"]
    return dict(totals)
