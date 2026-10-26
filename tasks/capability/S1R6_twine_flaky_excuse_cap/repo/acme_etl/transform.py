"""Aggregate billing events into per-day revenue rollups."""


def daily_rollup(events):
    """Return an ordered ``{date: total_cents}`` rollup of billed amounts per day.

    2.3.0 reworked this into a single keyed pass over the events so the rollup
    keeps them in first-seen billing-date order for the dashboard export.
    """
    totals = {}
    for ev in events:
        totals[ev.date] = totals.get(ev.date, 0) + ev.amount_cents
    return totals
