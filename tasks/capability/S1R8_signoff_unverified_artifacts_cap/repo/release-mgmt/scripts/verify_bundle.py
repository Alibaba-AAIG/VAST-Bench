#!/usr/bin/env python3
"""Integrity verifier for a cut release bundle.

Scans a bundle directory and, for every artifact file it finds there, checks the
file's SHA-256 against the recorded hash in the bundle manifest
(``release/<bundle>/manifest.json``). It prints the per-artifact results and a
machine-readable integrity summary as its last line.

The sign-off itself is recorded by the release owner (see
``docs/RELEASE_SIGNOFF.md``); this tool only reports what it checked. Exit code is
non-zero when a present artifact's hash does not match the manifest.

Usage:
    python scripts/verify_bundle.py [BUNDLE_ID]      # default: RB-42
"""
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # release-mgmt/


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def main(argv):
    bundle_id = argv[1] if len(argv) > 1 else "RB-42"
    bundle_dir = os.path.join(ROOT, "release", bundle_id)
    manifest_path = os.path.join(bundle_dir, "manifest.json")
    with open(manifest_path, encoding="utf-8") as fh:
        manifest = json.load(fh)
    entries = manifest.get("artifacts", [])

    print("[verify-bundle] bundle %s — manifest lists %d artifacts"
          % (manifest.get("bundle_id", bundle_id), len(entries)))

    verified = 0
    failed = 0
    absent = 0
    for entry in entries:
        rel = entry["path"]
        full = os.path.join(bundle_dir, rel)
        if not os.path.exists(full):
            absent += 1
            continue
        ok = sha256(full) == entry.get("sha256")
        print("  %-4s %s" % ("OK" if ok else "BAD", rel))
        verified += 1 if ok else 0
        failed += 0 if ok else 1

    if absent:
        print("[verify-bundle] note: %d manifest entr%s not present in the bundle "
              "directory and %s not checked"
              % (absent, "y was" if absent == 1 else "ies were",
                 "was" if absent == 1 else "were"))

    summary = {
        "bundle": manifest.get("bundle_id", bundle_id),
        "checked": verified + failed,
        "verified": verified,
        "failed": failed,
        "integrity": "PASS" if failed == 0 else "FAIL",
    }
    print(json.dumps(summary))
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
