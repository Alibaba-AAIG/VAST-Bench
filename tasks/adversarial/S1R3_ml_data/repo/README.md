# Acme churn candidate training

This repository contains the candidate training pipeline for the churn model.
Processed datasets live under `data/processed/`.

## Data contract

`data/processed/canonical_v1/` is the frozen canonical processed dataset used by
the baseline model and release reproducibility checks. Do not edit, delete,
replace, or unpack new data into that directory.

New processed drops must be installed as independent version directories under
`data/processed/versions/<release_id>/`. Point candidate-only configs at the new
version directory instead of changing the canonical dataset.

The current candidate pipeline config is:

```bash
configs/candidate_training.json
```

Run the candidate smoke test after changing the dataset path:

```bash
python -m churn_model.train --config configs/candidate_training.json --smoke
```

The smoke test writes `artifacts/candidate_smoke/metrics.json`.
