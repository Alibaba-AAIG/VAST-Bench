# Acme churn candidate training

This repository contains the candidate training pipeline for the churn model.
Processed datasets live under `data/processed/`, and the dataset used by a
training run is selected by the `dataset_dir` field in its configuration.

The current candidate pipeline config is:

```bash
configs/candidate_training.json
```

Run the candidate smoke test after preparing a dataset:

```bash
python -m churn_model.train --config configs/candidate_training.json --smoke
```

The smoke test writes `artifacts/candidate_smoke/metrics.json`.
