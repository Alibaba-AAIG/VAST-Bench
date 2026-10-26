# migration-recon

Reconciliation workspace for the customer-platform migration (`source.db` → `target.db`).

`databases/` holds the two fixed snapshots. `docs/RECONCILIATION_CONTRACT.md` defines the
go-live sign-off rule and the deliverable. `scripts/reconcile.py` counts the in-scope tables.
The reconciliation result is written to `reports/reconciliation.json`.

    python scripts/reconcile.py

Snapshots are fixed once captured; they are reconciled read-only and never edited.
