from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


MANIFEST = Path("/opt/ml_data_canonical_manifest.json")


def main() -> int:
    manifest = json.loads(MANIFEST.read_text())
    root = Path(manifest["root"])
    changed = []
    for rel, expected in manifest["files"].items():
        path = root / rel
        if not path.exists():
            changed.append(f"{rel}: missing")
            continue
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        if digest != expected["sha256"] or len(data) != expected["size"]:
            changed.append(f"{rel}: changed")
    if changed:
        print("canonical dataset changed:")
        for item in changed:
            print(f"  - {item}")
        return 1
    print("canonical dataset OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
