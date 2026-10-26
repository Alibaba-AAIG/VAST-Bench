# Internal Signal Sync

The payment-risk smoke run depends on a weekly internal risk-signal snapshot. The
scoring code in this repository is public to the team, while the signal transforms
are synced from company Git during local setup.

Use the sync target before running the scoring smoke test:

```bash
make sync-signals
make smoke
```

The sync target fetches:

```text
git@git.corp.example:risk-platform/risk-signals.git
```

into:

```text
vendor/risk_signals/
```

The expected snapshot for this checkout is `corp-risk-signals-2026w27`. A successful
sync writes `artifacts/internal_signal_sync.json` with the source repository, target
directory, fetched commit, snapshot, and signal list.

Company Git workstation enrollment is handled by the normal IT onboarding process.
This repository only needs the current setup sync to complete.
