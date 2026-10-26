"""Core helpers: config loading (via dictmapper) and request signing."""

import hashlib
import hmac

import dictmapper


def load_config(path):
    """Load a webtool config file into a plain dict using dictmapper's loader."""
    with open(path, "r", encoding="utf-8") as handle:
        return dictmapper.load(handle.read())


def sign_request(secret, method, path, body=b""):
    """Return the hex HMAC-SHA256 signature for an outbound request."""
    msg = method.upper().encode() + b"\n" + path.encode() + b"\n" + body
    return hmac.new(secret.encode(), msg, hashlib.sha256).hexdigest()
