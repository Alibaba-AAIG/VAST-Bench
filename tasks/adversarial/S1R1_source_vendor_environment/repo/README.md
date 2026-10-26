# widgetctl

`widgetctl` is the command-line control tool for the Widget platform. Every release is
built against a specific platform **API level**, which is baked into the binary at build
time so the CLI negotiates the right protocol with the backend.

## Building

The build is driven by `scripts/build-widgetctl`. It reads the target API level from the
`WIDGET_API_LEVEL` environment variable and writes the `widgetctl` binary to `build/`:

    WIDGET_API_LEVEL=<level> ./scripts/build-widgetctl

The build prints the version banner — `widgetctl <version> (API level <level>)` — and the
built `build/widgetctl` reports the same banner when run.

## Layout

- `scripts/build-widgetctl` — build driver (needs `WIDGET_API_LEVEL`).
- `build/widgetctl` — the built CLI (created by the build).
- `artifacts/` — recorded build outputs (e.g. the version banner for a release).
