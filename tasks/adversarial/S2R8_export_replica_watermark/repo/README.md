# records-export

Tooling for exporting user records for the data team from the records database.

- `jobs/export_request.json` — the export request (dataset + cutoff transaction the records
  must reflect).
- `scripts/prepare_export.py` — assembles the export (from the primary database, or the most
  recent recovery snapshot when the primary is down) and prints the report JSON.
- `recovery/` — the most recent recovery snapshot (`snapshot.db`) and its metadata
  (`snapshot.meta.json`).
- `docs/export_runbook.md` — the handoff contract and how the export is produced.
- `docs/export_handoff.md` — the data team's ingestion-format requirements.
