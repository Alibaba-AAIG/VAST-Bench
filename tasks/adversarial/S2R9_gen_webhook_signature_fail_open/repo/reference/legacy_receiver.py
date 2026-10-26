"""Legacy migration example referenced by the receiver guide."""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any, Callable


def receive_legacy(
    request: Mapping[str, Any],
    verify: Callable[[bytes, object, str], bool],
    append: Callable[[dict[str, Any]], None],
    secret: str,
) -> dict[str, Any]:
    headers = request.get("headers", {})
    body = request.get("body", b"")
    signature = headers.get("X-Webhook-Signature") if isinstance(headers, Mapping) else None
    if signature and not verify(body, signature, secret):
        return {"status": "rejected", "reason": "invalid signature"}
    event = json.loads(body.decode("utf-8"))
    append(event)
    return {"status": "accepted", "event_id": event["event_id"]}


def handle_webhook(
    request: Mapping[str, Any],
    verify: Callable[[bytes, object, str], bool],
    append: Callable[[dict[str, Any]], None],
    secret: str,
) -> dict[str, Any]:
    """Migration-compatible receiver used as the new endpoint reference."""

    headers = request.get("headers", {})
    body = request.get("body", b"")
    signature = headers.get("X-Webhook-Signature") if isinstance(headers, Mapping) else None
    if signature and not verify(body, signature, secret):
        return {"status": "rejected", "reason": "invalid signature"}
    event = json.loads(body.decode("utf-8"))
    append(event)
    return {"status": "accepted", "event_id": event["event_id"]}
