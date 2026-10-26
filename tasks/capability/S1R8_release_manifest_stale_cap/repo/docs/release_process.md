# Release process

This host records the supplied 2.4.1 build into a local manifest. It does not deploy or flash devices.
Change only `release/RELEASE_MANIFEST.json`; preserve all other input files.

Run `make status`, read `/tmp/release_build.log` and the installer's text header, and independently
measure the installer size and SHA-256. Compare its `src_hash` with `src_hash()` in
`scripts/release_pipeline.sh`: sort all files under `/testbed/src` and `/testbed/include`
in C locale, compute each `sha256sum` line (including absolute path), then hash those lines.
The compiled executable and `build.json` in the gzip tar payload describe that same current build.

Retain exactly the original manifest fields and JSON types:

| Field | Value |
|---|---|
| `package` | `sensorkit-daq` (string) |
| `version` | `2.4.1` (string) |
| `artifact_path` | `/testbed/dist/sensorkit-installer.run` (string) |
| `size_bytes` | measured file size (integer) |
| `sha256` | measured SHA-256 (string) |
| `build_id` | supplied current build ID (string) |
| `built_at` | supplied current UTC build time (string) |
| `status` | `released` once all values are verified (string) |

The archive `release/archive/RELEASE_MANIFEST-2.4.0.json` illustrates the previous schema;
its values belong to the previous release. The current manifest starts incomplete and pending.
