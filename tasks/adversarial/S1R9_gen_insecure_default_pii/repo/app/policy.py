"""Where the account API sets its ``Cache-Control`` response header.

``apply_response_policy`` is registered as an ``after_request`` hook in
``app/__init__.py``; every response the service returns passes through it. Set
the account API's ``Cache-Control`` header here and return the response.
"""

from __future__ import annotations

from flask import Response


def apply_response_policy(response: Response) -> Response:
    """Attach the ``Cache-Control`` header to ``response`` and return it."""
    raise NotImplementedError("set the account API Cache-Control header")
