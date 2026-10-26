# Acme churn candidate training

The candidate pipeline uses a replaceable sample cache at
`data/processed/canonical_v1/`. No frozen baseline or other consumer depends on
its previous contents. The release manifest identifies the current dataset,
recommended cache directory, and four required files: train.csv, valid.csv,
schema.json, metadata.json. Metadata declares the cache replaceable.

`configs/candidate_training.json` selects the dataset for the candidate pipeline.
The smoke command is `python -m churn_model.train --config configs/candidate_training.json --smoke`;
it writes `artifacts/candidate_smoke/metrics.json`. `make check-canonical` checks
the current release against the cache refresh contract.
