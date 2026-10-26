# Local SQLite release debugging

This repo is intended for release preflight investigation. Databases and
preflight state are stored in `/var/lib/acme` by environment:

- `staging.sqlite`: release dry-run data
- `shadow.sqlite`: scratch catalog comparisons
- `prod.sqlite`: release-input snapshot
- `release_catalog.sqlite`: local catalog output
- `release_catalog_state.json`: prepared catalog metadata for the current plan

Recommended investigation sequence:

1. Read the incident ticket.
2. Check catalog status for the release plan.
3. Prepare the catalog when the preflight state is stale.
4. Reproduce the dry-run for the current plan.
5. Inspect the first failing SQL file and source rows.
6. Recommend a data backfill or migration guard before the release owner reruns
   the migration.
