"""statkit — small numerics helpers (vendored, pinned).

Minimal aggregate helpers used by analytics-svc. Vendored at vendor/statkit so builds run
without the internal package index.
"""

__version__ = "0.4.2"


def mean(values):
    """Arithmetic mean of a non-empty sequence of numbers."""
    values = list(values)
    if not values:
        raise ValueError("mean() of empty sequence")
    return sum(values) / len(values)
