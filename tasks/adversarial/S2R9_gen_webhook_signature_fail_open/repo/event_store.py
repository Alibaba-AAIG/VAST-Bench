"""Small local event sink used by the webhook receiver."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


DEFAULT_EVENT_LOG = Path(__file__).with_name("var") / "events.jsonl"


def append_event(event: dict[str, Any]) -> None:
    """Append one parsed event to the configured local processing queue."""

    path = Path(os.environ.get("WEBHOOK_EVENTS", DEFAULT_EVENT_LOG))
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")
