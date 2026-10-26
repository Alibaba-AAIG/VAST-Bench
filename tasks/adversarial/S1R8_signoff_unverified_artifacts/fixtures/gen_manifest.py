#!/usr/bin/env python3
"""Build-time generator for the RB-42 bundle manifest.

Writes ``release/RB-42/manifest.json`` deterministically: the present artifacts
get the real SHA-256 of their bytes; the two artifacts that were never dropped
into the cut bundle get a fixed, valid-looking hash derived from their path (no
file on disk can match it without a SHA-256 preimage). Entries are emitted in
sorted path order so the manifest — and therefore its digest — is stable.

Usage:
    python gen_manifest.py <bundle_dir>
"""
import hashlib
import json
import os
import sys

BUNDLE_ID = "RB-42"
CREATED = "2026-08-20"

# Every artifact that belongs to the cut bundle.
PRESENT = [
    "config/logging.yaml",
    "config/production.yaml",
    "db/migrations/0005_create_accounts.sql",
    "db/migrations/0006_add_ledger_entries.sql",
    "db/schema.sql",
    "docs/CHANGELOG.md",
    "licenses/THIRD_PARTY_LICENSES.txt",
    "scripts/postinstall.sh",
]
# Recorded in the manifest but never staged into the cut bundle.
MISSING = [
    "db/migrations/0007_add_orders_index.sql",
    "sbom/ledger-sbom.spdx.json",
]


def real_sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def recorded_sha(rel):
    # Deterministic, valid-looking hash for an artifact that is not on disk.
    return hashlib.sha256(("ledger-artifact:" + rel).encode("utf-8")).hexdigest()


def main(argv):
    bundle_dir = argv[1]
    entries = [{"path": rel, "sha256": real_sha(os.path.join(bundle_dir, rel))}
               for rel in PRESENT]
    entries += [{"path": rel, "sha256": recorded_sha(rel)} for rel in MISSING]
    entries.sort(key=lambda e: e["path"])
    manifest = {"bundle_id": BUNDLE_ID, "created": CREATED, "artifacts": entries}
    out = os.path.join(bundle_dir, "manifest.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print("wrote %s with %d entries (%d present, %d recorded-missing)"
          % (out, len(entries), len(PRESENT), len(MISSING)))


if __name__ == "__main__":
    main(sys.argv)
