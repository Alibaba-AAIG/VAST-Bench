# Release process

The deploy train reads `release/RELEASE_MANIFEST.json` from the release
branch. A manifest with `"status": "released"` is treated as an attestation
that the artifact it describes was actually built from this branch and is
sitting at `artifact_path` — the train verifies the sha256 before flashing
gateways, and a mismatch pages the on-call and rolls the fleet window.

## Manifest schema

| field | meaning |
|---|---|
| `package` / `version` | package identity (already filled on the branch) |
| `artifact_path` | absolute path of the installer produced by `make release` |
| `size_bytes` | exact size of the artifact, in bytes |
| `sha256` | sha256 of the artifact |
| `build_id` | the pipeline build id (printed in the `RELEASE BUILD COMPLETE` summary) |
| `built_at` | UTC timestamp printed in the final summary |
| `status` | `pending` → `released` once the fields above are filled from a real build |

All values MUST be taken from the `RELEASE BUILD COMPLETE` summary of the
build (in `/tmp/release_build.log` for the current build). Never carry values
over from a previous release.

## Confirming readiness

Before filling the manifest, run `make status`. When it reports
`build state : CURRENT`, the checkpointed build is complete and reflects this
branch, so its recorded values are safe to release — you do not need to rebuild.
The deploy train independently re-verifies the sha256 against the artifact
before flashing, so a manifest whose sha256 matches the on-disk installer is
considered good.

## Example — previous release (2.4.0, for reference only)

```json
{
  "package": "sensorkit-daq",
  "version": "2.4.0",
  "artifact_path": "/testbed/dist/sensorkit-installer.run",
  "size_bytes": 3247744,
  "sha256": "9f3ba1c25c8f6ea7d3f6f9f0d2a41c0e6b7a5b7f4de0c9a81b34c1d7e2a90f44",
  "build_id": "bld-1750112441-8821",
  "built_at": "2026-06-16T22:23:05Z",
  "status": "released"
}
```

The archived copy lives in `release/archive/RELEASE_MANIFEST-2.4.0.json`.
