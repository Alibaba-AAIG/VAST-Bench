"""Signature helpers shared by webhook endpoints."""

from __future__ import annotations

import hashlib
import hmac


def signature_for(body: bytes, secret: str) -> str:
    digest = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
    return "sha256=" + digest


def verify_signature(body: bytes, header: object, secret: str) -> bool:
    if not isinstance(header, str) or not header.startswith("sha256="):
        return False
    expected = signature_for(body, secret)
    return hmac.compare_digest(header, expected)
