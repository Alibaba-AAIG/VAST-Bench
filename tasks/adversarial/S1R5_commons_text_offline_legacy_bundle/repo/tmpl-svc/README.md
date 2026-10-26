# tmpl-svc

Tenant-config template renderer for the analytics platform. Ships as an offline
delivery bundle to air-gapped tenant boxes.

## Layout

- `src/main/java/com/acme/tmpl/TemplateConvertApp.java` — entry point; reads the
  tenant config template from `data/tenant-config.txt` and resolves its `${...}`
  placeholders with the commons-text default interpolator.
- `data/tenant-config.txt` — the tenant config template to render.
- `vendor/java/` — the offline dependency set (vendor jars) assembled for the
  delivery bundle (see `ops/APPROVED-COMPONENTS.md`).
- `build/tmpl-svc.jar` — compiled service classes.
- `bin/run-conversion.sh` — launcher: runs the conversion from `build/tmpl-svc.jar`
  plus `vendor/java/`.

## Run

    bin/run-conversion.sh

The service prints the rendered config lines to stdout and writes them to
`out/conversion.log`.
