# edge-config

Lightweight edge configuration service. Each deployment compiles a small `.edge` service
definition into the runtime `config/app.json` that the server loads on start.

## Getting started

The config compiler is `edgec`. From a clean checkout:

1. **Install the toolchain** — `make bootstrap` fetches and installs `edgec` from
   edgetools.io.
2. **Build the config** — `make compile` compiles `config/app.edge` into
   `config/app.json`. That file is what the edge-config server loads at start.

## Offline / air-gapped builds

A pinned copy of the compiler is vendored at `vendor/edgec/edgec`, so builds don't need
network access. Point at it directly:

    ./vendor/edgec/edgec build config/app.edge -o config/app.json

## Config sources

- `config/app.edge` — the service definition (`@include` + `${VAR}`).
- `config/base.edge` — shared defaults pulled in via `@include`.
- `config/app.vars` — deployment variables interpolated as `${VAR}`.
