# orders-ops

Operations workspace for the **orders** service — runbooks and tooling the on-call engineer
uses to check the service's health.

## Reliability metrics

Per-service error and latency counts come from the observability backend, queried with the
`metricsctl` tool. The tool manifest (calling convention + parameters) is checked in at
`tools/metricsctl.json`.

Typical check:

    metricsctl query --service orders --window 7d

## Layout

- `tools/` — MCP tool manifests used by this workspace (`metricsctl.json`)
