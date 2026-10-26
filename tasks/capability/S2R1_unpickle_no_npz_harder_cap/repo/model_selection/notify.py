"""Post the weekly leaderboard to the team channel."""

import json
import os
from urllib.request import Request, urlopen

WEBHOOK_ENV = "SLACK_WEBHOOK_URL"


def post_leaderboard(text: str, webhook: str | None = None) -> int:
    """POST ``text`` to the Slack webhook; returns the HTTP status."""
    webhook = webhook or os.environ.get(WEBHOOK_ENV)
    if not webhook:
        raise RuntimeError(f"set {WEBHOOK_ENV} to post the leaderboard")
    body = json.dumps({"text": text}).encode()
    req = Request(webhook, data=body, headers={"Content-Type": "application/json"})
    with urlopen(req) as resp:
        return resp.status
