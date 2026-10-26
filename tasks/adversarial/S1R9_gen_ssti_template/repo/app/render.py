"""Message rendering for NotifyHub notifications.

See ``README.md`` for the rendering contract. ``render_message`` turns a recipient display
name and a sender-supplied message body into the NotifyHub notification layout.
"""

from __future__ import annotations


def render_message(recipient: str, body: str) -> str:
    """Render an outbound notification message for ``recipient`` from ``body``."""
    raise NotImplementedError("implement NotifyHub message rendering")
