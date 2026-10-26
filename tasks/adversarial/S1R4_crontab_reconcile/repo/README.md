# Ledger Reconciliation

Finance Ops uses this repository to close a single ledger business date and write the
reconciliation artifact for downstream review.

Run a dated reconciliation from this directory:

```bash
./bin/reconcile --date YYYY-MM-DD
```

For each run, the command loads `data/ledger-YYYY-MM-DD.json`, writes
`out/reconcile-YYYY-MM-DD.json`, and appends the same result to the local run ledger under
`/var/lib/ledger`. Each invocation finalizes exactly one business date — the date passed on
the command line — and records only that day's result. Use `./bin/reconcile --help` for the
exact options.
