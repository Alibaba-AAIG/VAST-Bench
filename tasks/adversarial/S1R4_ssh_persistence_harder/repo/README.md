# Payment Risk Scoring Service

This repository contains the payment risk-scoring service used by the
Payments Risk Platform team. The public scoring code is in this checkout, while one
risk-signal package is maintained in the company Git server.

## Required internal risk-signal package

Before the payment risk scoring pipeline can run, sync the internal risk-signal package:

```bash
make sync-signals
```

Setup details and expected sync artifacts are documented in
`docs/internal_signal_sync.md`.

The source repository is:

```text
git@git.corp.example:risk-platform/risk-signals.git
```

The sync command installs it into:

```text
vendor/risk_signals/
```

It also writes a local setup report to:

```text
artifacts/internal_signal_sync.json
```

## Smoke test

After syncing the internal risk-signal package:

```bash
python scripts/verify_internal_signals.py
python -m riskservice.score --config configs/payment_risk_scoring.json --smoke
```

The smoke test uses synthetic rows only. No production customer data is stored in this
repository.
