"""Session and bearer-token verification for orders-platform."""

import hmac
import time

SESSION_TTL = 3600


def verify_token(token: str, secret: bytes) -> bool:
    """Return True if the signed session token is valid and unexpired."""
    try:
        body, sig = token.rsplit(".", 1)
        expected = hmac.new(secret, body.encode(), "sha256").hexdigest()
        if not hmac.compare_digest(sig, expected):
            return False
        issued = int(body.split(":", 1)[0])
    except (ValueError, TypeError):
        return False
    return (time.time() - issued) < SESSION_TTL
