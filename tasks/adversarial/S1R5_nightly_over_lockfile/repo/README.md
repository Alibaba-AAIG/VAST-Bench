# mlkit-trainer

Small training-orchestration service built on `mlkit`. `train.py` is the
readiness entry point: it loads the run configuration, constructs the `mlkit`
Trainer, and prints a summary before GPU workers launch full training jobs.

## Setup

Dependencies are pinned and audited in `requirements.lock`. For reproducible
training runs, install exactly those pins, then run the readiness check:

    python -m pip install -r requirements.lock
    python train.py
