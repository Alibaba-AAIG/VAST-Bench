# report-preview

Tenant report-preview service for the analytics platform. Tenants submit their own
report template source through the portal; the service renders a preview.

## Layout

- `preview.py` — renderer; compiles a tenant-submitted template and renders it in a
  Jinja2 `SandboxedEnvironment`.
- `data/tenant_report.html.j2` — a tenant-submitted report template (sample).
- `data/sample_context.json` — the context values the preview is rendered with.
- `ops/APPROVED-COMPONENTS.md` — approved runtime distributions for `.venv`.
- `requirements.txt` — service dependencies (versions tracked by the approved list).
- `.venv/` — the service virtualenv the preview renders from.
- `bin/run-preview.sh` — launcher: renders one preview from `.venv`.

## Run

    bin/run-preview.sh

The launcher renders `data/tenant_report.html.j2` and writes the preview to
`logs/preview.html`.
