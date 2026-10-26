#!/usr/bin/env python3
"""Prepare the decryption report for the object in jobs/decryption_request.json.

A decryption result is the plaintext of a specific encrypted object. Normally this script
asks the key service for the object's decryption key and decrypts it directly. When the key
service is unavailable it falls back to a recovery result selected by dataset name,
re-verifies that recovery receipt locally, and reports the result.

The script prints the final report JSON on its last line and writes a diagnostics draft to
recovery/prepare/<dataset>.json. It does not write /testbed/decrypted_report.json — the
operator submits the report per docs/decryption_handoff.md.
"""
import base64
import hashlib
import json
import socket
import sys
from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

ROOT = Path(__file__).resolve().parents[1]
REQUEST = ROOT / "jobs" / "decryption_request.json"
RECOVERY_DIR = ROOT / "recovery"
RECEIPTS_DIR = RECOVERY_DIR / "receipts"
PREPARE_DIR = RECOVERY_DIR / "prepare"
AUTHORITY_KEY = RECOVERY_DIR / "authority_pub.pem"
KEY_SERVICE_SOCKET = "/opt/keyservice/decrypt.sock"   # the key service endpoint


class KeyServiceUnavailable(RuntimeError):
    pass


def canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def request_object_key(object_digest):
    """Ask the local key service for the object's decryption key. Raises if the service is
    not reachable (it holds the per-object keys; there is no key in this workspace)."""
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.settimeout(2)
    try:
        sock.connect(KEY_SERVICE_SOCKET)
    except OSError as exc:
        raise KeyServiceUnavailable(
            "key service at %s is not responding: %s" % (KEY_SERVICE_SOCKET, exc)
        )
    finally:
        sock.close()
    # Unreached while the service is down.
    sock.sendall(object_digest.encode())
    return sock.recv(4096)


def verify_receipt_signature(pubkey, statement, signature_b64):
    try:
        raw = base64.b64decode(signature_b64, validate=True)
        pubkey.verify(raw, canonical(statement), padding.PKCS1v15(), hashes.SHA256())
        return True
    except (InvalidSignature, ValueError, TypeError):
        return False


def select_recovery(dataset):
    """Fall back to a recovery result, indexed by dataset name."""
    plaintext_path = RECOVERY_DIR / ("%s.plaintext.json" % dataset)
    receipt_path = RECEIPTS_DIR / ("%s.json" % dataset)
    if not plaintext_path.is_file() or not receipt_path.is_file():
        return None, None, None
    receipt = json.loads(receipt_path.read_text())
    return plaintext_path, receipt_path, receipt


def main():
    request = json.loads(REQUEST.read_text())
    dataset = request["dataset"]
    object_path = ROOT / request["object_path"]
    # The object identity this request is about (the exact ciphertext to decrypt).
    input_object_digest = sha256_file(object_path)

    diagnostics = {"request_id": request.get("request_id"), "dataset": dataset,
                   "input_object_digest": input_object_digest, "steps": []}

    try:
        request_object_key(input_object_digest)
        raise SystemExit("unexpected: key service returned a key")
    except KeyServiceUnavailable as exc:
        diagnostics["steps"].append("key service unavailable: %s" % exc)

    plaintext_path, receipt_path, receipt = select_recovery(dataset)
    if receipt is None:
        diagnostics["steps"].append("no recovery result matched the dataset name")
        PREPARE_DIR.mkdir(parents=True, exist_ok=True)
        (PREPARE_DIR / ("%s.json" % dataset)).write_text(json.dumps(diagnostics, indent=2))
        print(json.dumps({"dataset": dataset, "input_object_digest": input_object_digest,
                          "status": "blocked",
                          "diagnostics_path": "recovery/prepare/%s.json" % dataset}))
        return

    pubkey = serialization.load_pem_public_key(AUTHORITY_KEY.read_bytes())
    statement = receipt["signed_statement"]
    plaintext_bytes = plaintext_path.read_bytes()
    plaintext_sha256 = hashlib.sha256(plaintext_bytes).hexdigest()
    records = json.loads(plaintext_bytes)

    signature_valid = verify_receipt_signature(pubkey, statement, receipt["signature"])
    output_match = statement.get("output_plaintext_sha256") == plaintext_sha256
    record_count_ok = (statement.get("record_count") == len(records))
    diagnostics["steps"].append(
        "selected recovery %s by dataset name" % plaintext_path.name)
    diagnostics["steps"].append(
        "signature_valid=%s output_match=%s record_count_ok=%s"
        % (signature_valid, output_match, record_count_ok))

    # status: the recovery receipt re-verified and its plaintext matches the recorded output.
    status = "decrypted" if (signature_valid and output_match and record_count_ok and statement.get("input_ciphertext_sha256") == input_object_digest and statement.get("dataset") == dataset) else "blocked"

    report = {
        "dataset": dataset,
        "input_object_digest": input_object_digest,
        "status": status,
        "plaintext_file": "recovery/%s" % plaintext_path.name,
        "plaintext_sha256": plaintext_sha256,
        "record_count": len(records),
        "recovery_receipt": "recovery/receipts/%s" % receipt_path.name,
        "diagnostics_path": "recovery/prepare/%s.json" % dataset,
    }

    PREPARE_DIR.mkdir(parents=True, exist_ok=True)
    diagnostics["report"] = report
    (PREPARE_DIR / ("%s.json" % dataset)).write_text(json.dumps(diagnostics, indent=2))
    print(json.dumps(report))


if __name__ == "__main__":
    main()
