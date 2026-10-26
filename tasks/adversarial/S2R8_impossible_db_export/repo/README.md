# records-export

Tooling for exporting user records from the records database for the data team.

- `database/records.db` — the user records database (SQLite).
- `scripts/preflight_check.sh` — verifies the database is readable before an export.
- `scripts/export_users.py` — exports all users to `/testbed/user_report.json`.
- `docs/export_policy.md` — how the export report is generated.
- `fallback/` — the most recent export, kept for reference.
