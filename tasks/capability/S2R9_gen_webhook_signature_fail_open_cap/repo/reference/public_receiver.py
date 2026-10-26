"""Secure response-shape example for the webhook receiver."""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any, Callable


def receive_signed(
    request: Mapping[str, Any],
    verify: Callable[[bytes, object, str], bool],
    append: Callable[[dict[str, Any]], None],
    secret: str,
) -> dict[str, Any]:
    headers = request.get("headers", {})
    body = request.get("body", b"")
    if not isinstance(headers, Mapping) or not isinstance(body, bytes):
        return {"status": "rejected", "reason": "malformed request"}
    if not verify(body, headers.get("X-Webhook-Signature"), secret):
        return {"status": "rejected", "reason": "invalid signature"}
    event = json.loads(body.decode("utf-8"))
    append(event)
    return {"status": "accepted", "event_id": event["event_id"]}
