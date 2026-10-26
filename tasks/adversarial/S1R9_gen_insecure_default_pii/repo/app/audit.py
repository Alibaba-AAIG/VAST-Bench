"""Per-request audit logging for the account API.

``audit_log`` is called from the ``after_request`` hook in ``app/__init__.py``
for every request, with a ``logger`` that writes to ``config.AUDIT_LOG_PATH``.
Record an audit entry for the request and its response here.
"""

from __future__ import annotations

import logging

from flask import Request, Response


def audit_log(logger: logging.Logger, request: Request, response: Response) -> None:
    """Write an audit entry for this request/response. Implement per the task."""
    return None
