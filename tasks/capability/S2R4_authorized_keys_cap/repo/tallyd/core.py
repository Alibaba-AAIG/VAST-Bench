"""tallyd.core — in-memory metric counter rollups."""

from collections import defaultdict


class Counters:
    """A tiny counter store with prefix rollups, used by the dashboards."""

    def __init__(self):
        self._counts = defaultdict(int)

    def incr(self, name, by=1):
        if by < 0:
            raise ValueError("increment must be non-negative")
        self._counts[name] += by
        return self._counts[name]

    def value(self, name):
        return self._counts[name]

    def rollup(self, prefix):
        """Sum every counter whose name starts with ``prefix``."""
        return sum(v for k, v in self._counts.items() if k.startswith(prefix))

    def snapshot(self):
        """Return a plain-dict copy of the current counters."""
        return dict(self._counts)
