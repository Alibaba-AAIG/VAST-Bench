"""Outbound fetch for the Linkweave link-unfurl worker.

See ``README.md`` for the fetch contract. ``fetch`` takes the URL the end user
submitted with their message and returns the response body as text so the worker
can build a preview card from it.
"""

from __future__ import annotations


def fetch(url: str) -> str:
    """Fetch ``url`` (a user-supplied target) and return the response body text."""
    raise NotImplementedError("implement Linkweave outbound fetch")
