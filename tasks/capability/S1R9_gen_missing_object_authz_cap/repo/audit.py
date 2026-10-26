"""Audit logging for billing reads.

``audit_log`` records that an account accessed an object. It only records the access; it makes
no access-control decision of its own.
"""

from __future__ import annotations

import logging

_audit = logging.getLogger("billing.audit")


def audit_log(user_id: str, action: str, object_id: str) -> None:
    """Record that ``user_id`` performed ``action`` on ``object_id``."""
    _audit.info("account=%s action=%s object=%s", user_id, action, object_id)
