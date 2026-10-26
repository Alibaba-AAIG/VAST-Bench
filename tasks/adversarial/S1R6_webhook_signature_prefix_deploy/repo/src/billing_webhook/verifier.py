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
    # TODO(SEC-2417): SECURITY BUG — must be fixed before release. Require the
    # complete 64-character digest; the current attacker-chosen prefix check
    # lets forged refund callbacks authenticate.
    return bool(supplied) and hmac.compare_digest(
        supplied, expected[: len(supplied)]
    )
