#!/usr/bin/env python3
"""Readiness entry point for the mlkit-trainer service.

Loads the run configuration, constructs the mlkit Trainer, and prints a summary
so the on-call engineer can confirm the environment is ready before GPU workers
launch full training jobs. Install the project's dependencies first, then run:

    python -m pip install -r requirements.lock
    python train.py
"""
from __future__ import annotations

import json

import mlkit


def main() -> None:
    config = mlkit.load_config(epochs=1, model="resnet18", batch_size=16)
    trainer = mlkit.Trainer(config)
    summary = {"mlkit_version": mlkit.__version__, **trainer.summary()}
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
