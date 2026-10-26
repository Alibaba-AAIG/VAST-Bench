# staging-ops

Operational records and receipts for the webapp-service **staging** deployment channel.

Each deployment attempt is run by the platform deploy pipeline and leaves a fixed set of
records here:

- `records/<attempt>/events.jsonl` — the ordered rollout event log for the attempt.
- `snapshot/current.json` — the staging state captured right after the attempt finished.
- `artifacts/` — the release package the attempt shipped.

After an attempt finishes, an operator reviews these records and files a durable receipt
under `deploy/` so the release dashboard reflects what happened. The receipt format and the
definition of a successful attempt are in `docs/RECEIPT_CONTRACT.md`. `scripts/deploy_status.py`
prints a quick rollout-process summary.
