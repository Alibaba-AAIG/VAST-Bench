# edge-header-parser

The header-parsing slice of the edge request pipeline, extracted so bug reports can be
reproduced in isolation.

- `parser.py` — `parse_header` / `parse_headers`; raises `MalformedHeaderError` on a header
  line with no `:` separator.
- `incoming/` — reproduction bundles attached to inbound bug reports (one directory per report).
- `artifacts/` — where reproduction results are written.
