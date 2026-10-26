"""Aggregate request-metric samples into per-route rollups."""


def rollup_by_route(samples):
    """Return an ordered ``{route: total_requests}`` rollup of request counts.

    1.4.0 reworked this into a single keyed pass over the samples so the rollup
    keeps them in first-seen route order for the dashboard export.
    """
    totals = {}
    for s in samples:
        totals[s.route] = totals.get(s.route, 0) + s.requests
    return totals
