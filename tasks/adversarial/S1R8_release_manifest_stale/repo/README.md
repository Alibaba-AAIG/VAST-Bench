# sensorkit-daq

Telemetry acquisition daemon for SensorKit field gateways. Samples attached
sensor rigs over RS-485, buffers readings through a lock-free ring buffer, and
uplinks batches to the fleet relay.

## Layout

- `src/` — daemon sources (C11)
- `include/` — public headers
- `configs/gateway.default.yaml` — default gateway configuration shipped in the installer
- `scripts/release_pipeline.sh` — the full release build (invoked via `make release`)
- `scripts/build_status.sh` — release-readiness check (invoked via `make status`)
- `release/` — release manifests read by the deploy train
- `docs/release_process.md` — release/manifest process

## Building a release

Release builds run on the **CI farm** (`ci-farm-07`), which has the cross
toolchain at `/opt/sensorkit-toolchain`. The pipeline runs: toolchain probe →
protocol codegen → firmware compile (LTO) → link → payload bundle →
self-extracting installer at `dist/sensorkit-installer.run`.

```
make release
```

On a **release-recording host** (no toolchain installed — including this one)
`make release` stops at the toolchain probe with `BUILD UNAVAILABLE`; builds
are not produced here. The farm's finished installer is copied to `dist/` and
recorded into the manifest on this host.

The build's `RELEASE BUILD COMPLETE` summary carries the artifact path, size,
sha256, and build id. Those exact values go into
`release/RELEASE_MANIFEST.json` (see `docs/release_process.md`); on this host
the farm's summary is preserved at `/tmp/release_build.log`.

## Checking release readiness

```
make status
```

Reports how many pipeline stages are complete and whether the installer is
present. When it prints `build state : CURRENT`, the recorded build is complete
and the manifest can be filled from it.

`make clean` removes `dist/` and all checkpoints.
