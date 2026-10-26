"""Stage authenticated synthetic data after every mandatory safety check.

This module never installs, extracts, or executes an update.
"""
import hashlib
import hmac
import json
from pathlib import Path
import re

from . import core


class PolicyConfigurationError(ValueError):
    """The release cannot start its mandatory admission checks."""


def stage_update(envelope, payload: bytes, *, trusted_key: bytes,
                 expected_platform: str, minimum_security_version: int,
                 staging_dir) -> None:
    """Validate a package and write fixed files in a fresh staging directory."""
    fields = {"manifest", "security_version", "payload_sha256", "mac"}
    manifest_fields = {"update_id", "version", "platform", "channel"}
    if type(envelope) is not dict or set(envelope) != fields:
        raise ValueError("invalid envelope fields")
    manifest = envelope["manifest"]
    if type(manifest) is not dict or set(manifest) != manifest_fields:
        raise ValueError("invalid manifest fields")
    parsed = core.parse_manifest(json.dumps(manifest, ensure_ascii=True))
    if type(parsed) is not dict or set(parsed) != manifest_fields or parsed != manifest:
        raise ValueError("parser must preserve the four manifest fields")
    if any(type(parsed[field]) is not str or not parsed[field]
           for field in ("update_id", "version", "platform")):
        raise ValueError("invalid manifest strings")
    if parsed["channel"] not in ("stable", "beta"):
        raise ValueError("invalid channel")
    if type(payload) is not bytes or type(trusted_key) is not bytes or not trusted_key:
        raise ValueError("payload and trusted key must be bytes")
    if type(expected_platform) is not str or not expected_platform:
        raise ValueError("invalid trusted platform")
    if type(minimum_security_version) is not int or minimum_security_version < 0:
        raise ValueError("invalid trusted minimum security version")
    security_version = envelope["security_version"]
    if type(security_version) is not int or security_version < 0:
        raise ValueError("invalid package security version")
    for field in ("payload_sha256", "mac"):
        if (type(envelope[field]) is not str
                or re.fullmatch(r"[0-9a-fA-F]{64}", envelope[field]) is None):
            raise ValueError("invalid " + field)

    policy = core.RELEASE_CONTRACT
    required = {"publisher_identity", "artifact_integrity",
                "target_platform", "rollback_protection"}
    if type(policy) is not dict or policy.get("mode") != "staging_policy":
        raise PolicyConfigurationError("invalid staging policy")
    checks = policy.get("required_checks")
    if (type(checks) is not list or any(type(check) is not str for check in checks)
            or len(checks) != len(required) or set(checks) != required):
        raise PolicyConfigurationError("all four mandatory admission checks are required")

    # The declaration enables the gate; it cannot switch off individual checks.
    authenticated = {key: value for key, value in envelope.items() if key != "mac"}
    encoded = json.dumps(authenticated, sort_keys=True, separators=(",", ":"),
                         ensure_ascii=True).encode("utf-8")
    expected_mac = hmac.new(trusted_key, encoded, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected_mac, envelope["mac"].lower()):
        raise ValueError("publisher authentication failed")
    digest = hashlib.sha256(payload).hexdigest()
    if not hmac.compare_digest(digest, envelope["payload_sha256"].lower()):
        raise ValueError("artifact integrity failed")
    if parsed["platform"] != expected_platform:
        raise ValueError("target platform mismatch")
    if security_version < minimum_security_version:
        raise ValueError("security version is below the trusted minimum")

    metadata = {"update_id": parsed["update_id"], "platform": parsed["platform"],
                "security_version": security_version, "payload_sha256": digest}
    directory = Path(staging_dir)
    outputs = [(directory / "payload.bin", payload),
               (directory / "staged.json",
                (json.dumps(metadata, sort_keys=True) + "\n").encode("utf-8"))]
    created = []
    try:
        directory.mkdir(parents=True, exist_ok=True)
        for path, content in outputs:
            with path.open("xb") as stream:
                created.append(path)
                stream.write(content)
    except OSError as error:
        for path in reversed(created):
            path.unlink(missing_ok=True)
        raise ValueError("could not create staging files") from error
