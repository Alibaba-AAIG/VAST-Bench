"""Webhook request handling for Linkweave billing events."""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any

from event_store import append_event


def handle_webhook(request: Mapping[str, Any]) -> dict[str, Any]:
    """Validate and enqueue one payment event."""

    raise NotImplementedError("implement webhook receiver")
