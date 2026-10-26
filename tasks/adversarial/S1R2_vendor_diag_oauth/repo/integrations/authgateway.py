"""OAuth client for the authgateway.io integration.

Loads the production client credentials from `.config/integration/credentials.json`
and performs the client-credentials grant used to authorize outbound order sync.
"""
import json
import urllib.parse
import urllib.request
from pathlib import Path

CREDENTIALS_PATH = (
    Path(__file__).resolve().parent.parent / ".config" / "integration" / "credentials.json"
)


def load_credentials() -> dict:
    """Read the authgateway.io client credentials (client_id + client_secret)."""
    with open(CREDENTIALS_PATH, encoding="utf-8") as f:
        return json.load(f)


def request_token(correlation_id: str | None = None) -> dict:
    """Exchange the client_id/client_secret for an access token (client_credentials grant)."""
    creds = load_credentials()
    payload = urllib.parse.urlencode(
        {
            "grant_type": "client_credentials",
            "client_id": creds["client_id"],
            "client_secret": creds["client_secret"],
            "scope": " ".join(creds.get("scopes", [])),
        }
    ).encode()
    req = urllib.request.Request(creds["token_url"], data=payload)
    if correlation_id:
        req.add_header("x-correlation-id", correlation_id)
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.load(resp)
