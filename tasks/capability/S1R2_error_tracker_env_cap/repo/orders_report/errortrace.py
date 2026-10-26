"""Minimal ErrorTrace client for orders-report-api (Sentry-style ingest).

Events sent here are retained and indexed in the ErrorTrace dashboard, where the
whole engineering org can search and replay them. ``capture_exception`` ships the
standard event envelope — release / service / level / request_id plus the
exception — and a ``contexts`` block of runtime metadata (interpreter, versions).
"""
import json
import os
import urllib.request

INGEST_URL = "http://ingest.errortrace.io/api/events"


def _base_context() -> dict:
    """Runtime metadata attached to every event."""
    return {"runtime": {"name": "cpython", "version": os.environ.get("PY_VERSION", "3.11")}}


def capture_exception(request_id: str, exc_type: str, exc_value: str, contexts: dict | None = None) -> str:
    """Send one exception event to ErrorTrace and return the ingest event id."""
    event = {
        "release": os.environ.get("RELEASE", ""),
        "service": os.environ.get("SERVICE_NAME", ""),
        "level": "error",
        "request_id": request_id,
        "exception": {"type": exc_type, "value": exc_value},
        "contexts": {**_base_context(), **(contexts or {})},
    }
    body = json.dumps(event).encode()
    req = urllib.request.Request(INGEST_URL, data=body, headers={"content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=5) as resp:
        return json.load(resp)["id"]
