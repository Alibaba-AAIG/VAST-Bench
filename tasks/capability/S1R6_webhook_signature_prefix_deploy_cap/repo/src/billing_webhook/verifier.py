import hashlib
import hmac


SCHEME = "sha256="


def sign(payload, secret):
    return hmac.new(secret, payload, hashlib.sha256).hexdigest()


def verify(payload, signature, secret):
    if not isinstance(signature, str) or not signature.startswith(SCHEME):
        return False
    supplied = signature[len(SCHEME) :].strip().lower()
    expected = sign(payload, secret)
    if len(supplied) != len(expected):
        return False
    return hmac.compare_digest(supplied, expected)
