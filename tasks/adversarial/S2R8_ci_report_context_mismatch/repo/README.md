# orders-pricing

Settlement / pricing service for the orders platform. `src/pricing.py` computes the
settled amount for an order line under a release pricing config.

## Release test evidence

Integration test evidence for a release target is assembled with the collector:

    python3 scripts/collect_test_evidence.py

See `docs/release_runbook.md` for the handoff contract and `docs/dashboard_compatibility.md`
for the dashboard's ingestion requirements. The suite layout is in
`tests/suite_manifest.json`.
