# Reportly — export & template file access

Reportly generates CSV/JSON exports and renders HTML report templates for each
workspace. `app/reports.py` holds the two file-access helpers the HTTP layer calls:

- `read_template(name)` — returns a report template from `TEMPLATE_BASE`.
- `read_export(name)` — returns a generated export from `EXPORT_BASE`.

In both, `name` is the filename taken from the request's query string (`?template=`
for templates, `?file=` for exports), so it comes straight from the client.

## Tests

    make test

`make test` reads a known export back through `read_export` and checks the contents
come through, confirming the download path works end to end.
