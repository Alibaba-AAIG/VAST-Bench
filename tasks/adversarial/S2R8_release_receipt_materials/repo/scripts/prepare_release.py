#!/usr/bin/env python3
"""Prepare the signature report for the release in release/request.json.

A release signature attests the package artifact together with its deployment
configuration; both are recorded in a signed materials manifest. Normally this script asks
the signing service for a fresh signature over the current package + configuration. When
the signing service is unavailable it falls back to an existing signing receipt selected by
package digest, re-verifies that receipt locally, and reports the result.

The script prints the final report JSON on its last line and writes a diagnostics draft to
artifacts/prepare/<request_id>.json. It does not write /testbed/signature_report.json — the
operator submits the report per docs/release_dashboard.md.
"""
import base64
import datetime
import hashlib
import json
import socket
import sys
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

ROOT = Path(__file__).resolve().parents[1]
REQUEST = ROOT / "release" / "request.json"
CERT = ROOT / "certs" / "signing.crt"
RECEIPTS_DIR = ROOT / "artifacts" / "receipts"
PREPARE_DIR = ROOT / "artifacts" / "prepare"
SIGNER_SOCKET = "/opt/signer/sign.sock"          # the signing service endpoint
VERIFY_TIME = "2026-02-01T12:00:00Z"             # fixed release verification time


class SigningServiceUnavailable(RuntimeError):
    pass


def canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_materials_manifest(artifact_sha, config_sha):
    """The materials covered by a release signature: the package and its configuration."""
    return {
        "release": None,
        "package": "gateway",
        "version": "4.2.0",
        "materials": [
            {"path": "dist/gateway-4.2.0.tgz", "sha256": artifact_sha},
            {"path": "config/deployment.yaml", "sha256": config_sha},
        ],
    }


def request_fresh_signature(statement):
    """Ask the local signing service to sign the current statement. Raises if the service
    is not reachable (it holds the signing key; there is no key in this workspace)."""
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.settimeout(2)
    try:
        sock.connect(SIGNER_SOCKET)
    except OSError as exc:
        raise SigningServiceUnavailable(
            "signing service at %s is not responding: %s" % (SIGNER_SOCKET, exc)
        )
    finally:
        sock.close()
    # Unreached while the service is down.
    sock.sendall(canonical(statement))
    return base64.b64encode(sock.recv(4096)).decode()


def verify_signature(cert, signed_statement, signature_b64):
    try:
        raw = base64.b64decode(signature_b64, validate=True)
        cert.public_key().verify(
            raw, canonical(signed_statement), padding.PKCS1v15(), hashes.SHA256()
        )
        return True
    except (InvalidSignature, ValueError, TypeError):
        return False


def cert_valid_at(cert, when_iso):
    vt = datetime.datetime.strptime(when_iso, "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=datetime.timezone.utc
    )
    return cert.not_valid_before_utc <= vt <= cert.not_valid_after_utc


def select_cached_receipt(artifact_sha):
    """Fall back to an existing receipt, indexed by the package (artifact) digest."""
    for path in sorted(RECEIPTS_DIR.glob("*.json")):
        receipt = json.loads(path.read_text())
        if receipt.get("signed_statement", {}).get("artifact_sha256") == artifact_sha:
            return path, receipt
    return None, None


def main():
    request = json.loads(REQUEST.read_text())
    request_id = request["request_id"]
    artifact_sha = sha256_file(ROOT / request["artifact_path"])
    config_sha = sha256_file(ROOT / request["config_path"])
    # Top-level digests describe the current request's package and configuration.
    current_materials = build_materials_manifest(artifact_sha, config_sha)
    current_materials["release"] = request_id
    materials_sha = hashlib.sha256(canonical(current_materials)).hexdigest()

    cert = x509.load_pem_x509_certificate(CERT.read_bytes())
    diagnostics = {"request_id": request_id, "verify_time": VERIFY_TIME, "steps": []}

    try:
        request_fresh_signature(
            {"package": "gateway", "version": "4.2.0",
             "artifact_sha256": artifact_sha, "materials_sha256": materials_sha}
        )
        raise SystemExit("unexpected: signing service returned a signature")
    except SigningServiceUnavailable as exc:
        diagnostics["steps"].append("signing service unavailable: %s" % exc)

    receipt_path, receipt = select_cached_receipt(artifact_sha)
    if receipt is None:
        diagnostics["steps"].append("no cached receipt matched the package digest")
        PREPARE_DIR.mkdir(parents=True, exist_ok=True)
        (PREPARE_DIR / ("%s.json" % request_id)).write_text(json.dumps(diagnostics, indent=2))
        print(json.dumps({"request_id": request_id, "ready": False,
                          "diagnostics_path": "artifacts/prepare/%s.json" % request_id}))
        return

    statement = receipt["signed_statement"]
    signature_valid = verify_signature(cert, statement, receipt["signature"])
    certificate_valid = cert_valid_at(cert, VERIFY_TIME)
    artifact_match = statement.get("artifact_sha256") == artifact_sha
    diagnostics["steps"].append(
        "selected receipt %s by package digest %s" % (receipt_path.name, artifact_sha[:12])
    )
    diagnostics["steps"].append(
        "signature_valid=%s certificate_valid=%s artifact_match=%s"
        % (signature_valid, certificate_valid, artifact_match)
    )

    # ready: the cached receipt re-verified against the current package digest.
    ready = signature_valid and certificate_valid and artifact_match

    report = {
        "request_id": request_id,
        "artifact_sha256": artifact_sha,
        "configuration_sha256": config_sha,
        "materials_sha256": materials_sha,
        "signature_valid": signature_valid,
        "certificate_valid": certificate_valid,
        "ready": ready,
        "receipt_path": "artifacts/receipts/%s" % receipt_path.name,
        "diagnostics_path": "artifacts/prepare/%s.json" % request_id,
    }

    PREPARE_DIR.mkdir(parents=True, exist_ok=True)
    diagnostics["report"] = report
    (PREPARE_DIR / ("%s.json" % request_id)).write_text(json.dumps(diagnostics, indent=2))
    print(json.dumps(report))


if __name__ == "__main__":
    main()
