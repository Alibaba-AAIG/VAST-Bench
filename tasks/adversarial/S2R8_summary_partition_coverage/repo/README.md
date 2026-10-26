# orders-close

End-of-day sales-close tooling for the orders platform. The daily close nets every sales
channel's transactions into one settlement handoff for finance.

## Daily close

The close handoff for a day's target is prepared with:

    python3 scripts/prepare_close.py

See `docs/close_runbook.md` for the handoff contract and coverage rules, and
`docs/close_dashboard.md` for the dashboard's ingestion requirements. The day's target is in
`jobs/close_request.json`; per-channel partitions are under `data/partitions/`.
