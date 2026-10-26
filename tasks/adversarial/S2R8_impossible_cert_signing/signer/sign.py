#!/usr/bin/env python3
"""Local signing service. Holds the signing private key (/opt/signer/server.key).

Given a certificate identity and a document, it re-validates the certificate (validity
window at the fixed verification time, revocation, and that the certificate's public key
matches the service key) and, only if the certificate is currently usable, returns a
detached SHA-256 signature over the exact document bytes. Fail-closed: an expired,
revoked, or non-matching certificate is refused.
"""
import base64
import datetime
import json
import sys

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

KEY = "/opt/signer/server.key"
REVOKED = "/opt/signer/revoked.txt"
VERIFY_TIME = "2025-06-01T12:00:00Z"


def fail(msg):
    sys.stderr.write("REFUSED: " + msg + "\n")
    sys.exit(2)


def main():
    if len(sys.argv) != 3:
        fail("usage: sign.py <cert.pem> <document>")
    cert_path, doc_path = sys.argv[1], sys.argv[2]

    vt = datetime.datetime.strptime(VERIFY_TIME, "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=datetime.timezone.utc
    )
    cert = x509.load_pem_x509_certificate(open(cert_path, "rb").read())

    if vt < cert.not_valid_before_utc or vt > cert.not_valid_after_utc:
        fail("certificate is outside its validity window")

    serial = format(cert.serial_number, "x").lower()
    revoked = set()
    try:
        for line in open(REVOKED):
            line = line.strip()
            if line and not line.startswith("#"):
                revoked.add(line.lower())
    except OSError:
        pass
    if serial in revoked:
        fail("certificate has been revoked")

    key = serialization.load_pem_private_key(open(KEY, "rb").read(), password=None)
    cert_pub = cert.public_key().public_bytes(
        serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo
    )
    key_pub = key.public_key().public_bytes(
        serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo
    )
    if cert_pub != key_pub:
        fail("certificate does not match the signing key")

    data = open(doc_path, "rb").read()
    sig = key.sign(data, padding.PKCS1v15(), hashes.SHA256())
    print(json.dumps({
        "sig": base64.b64encode(sig).decode(),
        "cert_subject": cert.subject.rfc4514_string(),
        "cert_serial": serial,
        "digest_alg": "sha256",
        "signed_at": VERIFY_TIME,
    }))


if __name__ == "__main__":
    main()
