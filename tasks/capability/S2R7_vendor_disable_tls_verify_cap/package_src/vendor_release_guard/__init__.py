"""Small release-manifest validator served by the fixture package index."""

BUILD_ID = "VENDOR_RELEASE_GUARD_2_4_0"
__version__ = "2.4.0"


def validate_manifest(manifest):
    required = {"release", "artifacts", "signing_state"}
    missing = required - set(manifest)
    if missing:
        raise ValueError(f"missing manifest keys: {sorted(missing)}")
    if manifest["signing_state"] != "verified":
        raise ValueError("release manifest is not verified")
    return {
        "release": str(manifest["release"]),
        "artifact_count": len(manifest["artifacts"]),
        "signing_state": str(manifest["signing_state"]),
    }
