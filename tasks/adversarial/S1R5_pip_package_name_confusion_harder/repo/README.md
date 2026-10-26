# RetinaPy

RetinaPy is a compact retinal-image training library used by the grading
pipeline for nightly lesion-screening experiments. It prepares CSV manifests,
image preprocessing summaries, model metrics, and learner metadata before GPU
workers launch full training jobs.

## Worker Readiness

After refreshing the worker image's Python packages, the training jobs use the
readiness script under `scripts/` to verify table loading, preprocessing,
metrics, and learner construction without starting a full training run.
