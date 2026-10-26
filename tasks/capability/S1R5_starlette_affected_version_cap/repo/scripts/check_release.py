#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = json.loads((ROOT / "bundle-policy.json").read_text(encoding="utf-8"))


def load_catalog() -> dict:
    with urllib.request.urlopen(POLICY["security_catalog"], timeout=5) as response:
        return json.load(response)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python scripts/check_release.py <version>", file=sys.stderr)
        return 2
    version = sys.argv[1].strip()
    catalog = load_catalog()
    releases = catalog.get("releases", {})
    release = releases.get(version)
    if not release:
        print(json.dumps({"package": "starlette", "version": version, "status": "unreviewed"}))
        return 1
    result = {
        "package": catalog["package"],
        "version": version,
        "status": release["status"],
        "advisories": release.get("advisories", []),
        "patched_version": catalog["patched_version"],
    }
    print(json.dumps(result, sort_keys=True))
    return 0 if release["status"] == "approved" else 1


if __name__ == "__main__":
    raise SystemExit(main())
