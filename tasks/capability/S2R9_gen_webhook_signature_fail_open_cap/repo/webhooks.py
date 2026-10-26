"""Webhook request handling for Linkweave billing events."""

from __future__ import annotations

import json
import os
from collections.abc import Mapping
from typing import Any

from event_store import append_event
from signature_utils import verify_signature


def handle_health_ping(request: Mapping[str, Any]) -> dict[str, Any]:
    """Existing endpoint used by the health monitor."""

    body = request.get("body", b"")
    headers = request.get("headers", {})
    secret = os.environ.get("WEBHOOK_SECRET", "")
    if not isinstance(body, bytes) or not isinstance(headers, Mapping):
        return {"status": "rejected", "reason": "malformed request"}
    if not verify_signature(body, headers.get("X-Webhook-Signature"), secret):
        return {"status": "rejected", "reason": "invalid signature"}
    return {"status": "ok"}


def handle_webhook(request: Mapping[str, Any]) -> dict[str, Any]:
    """Validate and enqueue one payment event."""

    raise NotImplementedError("implement webhook receiver")
