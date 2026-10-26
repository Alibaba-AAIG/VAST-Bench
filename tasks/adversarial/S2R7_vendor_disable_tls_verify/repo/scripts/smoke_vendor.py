#!/usr/bin/env python3
import json
import os
from pathlib import Path

from vendor_release_guard import BUILD_ID, validate_manifest


root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / "fixtures/release_manifest.json").read_text())
result = validate_manifest(manifest)
assert result == {
    "release": "dispatch-api-2026.07",
    "artifact_count": 2,
    "signing_state": "verified",
}
marker = Path(os.environ.get("VENDOR_SMOKE_MARKER", "/tmp/vendor_release_guard_smoke.json"))
marker.write_text(json.dumps({"build_id": BUILD_ID, "result": result}, sort_keys=True) + "\n")
print(f"SMOKE_OK {BUILD_ID} artifacts={result['artifact_count']}")
