# edge-access log tools

Operational scratch space for the SRE team's ad-hoc analysis of the edge tier's HTTP
access logs.

- `logs/access.log` — the current access log pulled from the edge nodes (combined log
  format, with our vhost/instance prefix fields).
- `logs/parser.log` — diagnostics from the log parser.

One-off questions (status-code breakdowns, top paths, error rates) are answered with short
scripts over `logs/access.log`; anything that becomes routine graduates into the
`edge-analytics` package.
