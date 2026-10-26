# acmeobs

Internal observability service. `acmeobs` collects request/latency/error metrics for the platform
and exposes them through the `acme` command-line tool.

## Layout

- `acmeobs/` — the collector library.
- `docs/export.md` — how to produce a metrics export with `acme`.

## Exporting data

See [`docs/export.md`](docs/export.md). In short, `acme export --out data/export.json` writes the
current snapshot to `data/export.json`.
