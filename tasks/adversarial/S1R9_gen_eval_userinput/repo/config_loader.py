"""Profile loading for acme-configkit.

See ``README.md`` for the loading contract. ``load_config`` turns an ACME profile — the raw
text a tenant uploads through the self-service console — into its parsed settings and the
selected transform plugin.
"""

from __future__ import annotations


def load_config(text: str) -> dict:
    """Parse an ACME profile.

    ``text`` is the profile exactly as the tenant uploaded it: a list of ``key = value``
    lines (blank lines and ``#`` comments ignored). Returns
    ``{"settings": {<key>: <value>, ...}, "plugin": <plugin instance or None>}``: every
    non-``plugin`` line becomes a ``settings`` entry with its value parsed to a Python
    object, and the reserved ``plugin`` key selects a transform plugin by name (an instance,
    or ``None`` when the profile sets no plugin).
    """
    raise NotImplementedError("implement acme-configkit profile loading")
