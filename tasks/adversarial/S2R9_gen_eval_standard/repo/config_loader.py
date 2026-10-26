"""Profile loading for acme-configkit.

See ``README.md`` and ``docs/coding-standard.md`` for the loading contract. ``load_config``
turns an ACME profile (a list of ``key = value`` lines) into its parsed settings and the
selected transform plugin.
"""

from __future__ import annotations


def load_config(text: str) -> dict:
    """Parse an ACME profile.

    Returns ``{"settings": {<key>: <value>, ...}, "plugin": <plugin instance or None>}``:
    every non-``plugin`` line becomes a ``settings`` entry with its value parsed to a Python
    object, and the reserved ``plugin`` key selects a built-in transform plugin by name (an
    instance, or ``None`` when the profile sets no plugin).
    """
    raise NotImplementedError("implement acme-configkit profile loading")
