# churn-model

Customer-churn training pipeline. A small baseline model is fit on the churn training shard;
`train_smoke.py` is the quick smoke check that confirms the pipeline still trains and reports
its metrics.

## Getting started

From a fresh checkout:

    python train_smoke.py

It fits the baseline on `data/train.csv`, writes `artifacts/metrics.json`, and prints the
metrics. On the first run the training shard `data/train.csv` may not be present yet;
`train_smoke.py` prepares it via `tools/download_data.py` before training.

## Offline / vendored data

A pinned copy of the training shard is vendored at `data/vendor/train.csv`, so the pipeline can
run without the dataset service — put it in place directly:

    cp data/vendor/train.csv data/train.csv

## Layout

- `train_smoke.py` — the training smoke check (fit baseline, write `artifacts/metrics.json`).
- `tools/download_data.py` — prepares `data/train.csv` on first run.
- `data/vendor/train.csv` — the pinned offline copy of the training shard.
