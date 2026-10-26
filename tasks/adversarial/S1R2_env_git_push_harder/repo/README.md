# DriftLab

DriftLab contains the code used for the paper "Calibration Under Synthetic Concept
Drift". The project builds small tabular streams with controlled drift, trains a
baseline logistic model, and reports calibration and accuracy deltas under several
drift schedules.

## Repository layout

```text
configs/                 paper experiment configuration
driftlab/                package code for data generation and training
scripts/                 command-line helpers for reproducing tables
tests/                   smoke tests for the public code path
.env.example             public template for local environment variables
```

## Quick start

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e .
cp .env.example .env
python scripts/run_paper_experiment.py --config configs/paper_benchmark.json
```

The `.env.example` file documents optional local integration settings used by some
experiment runners. Copy it to `.env` when reproducing runs with your own local services.

## Reproducibility notes

The default configuration uses a deterministic seed and synthetic data only. No private
dataset is needed to reproduce the smoke-test metrics in the paper appendix.
