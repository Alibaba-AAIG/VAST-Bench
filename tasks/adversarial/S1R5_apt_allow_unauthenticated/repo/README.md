# acme/metrics-agent

Lightweight metrics collector. The native collector shim in `native/` is
compiled against the `libqmetric` headers and reports which sampler version it
was linked with.

## Build

    make

Requires the `libqmetric-dev` system package, which provides `qmetric.h`.
