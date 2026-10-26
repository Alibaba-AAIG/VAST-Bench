# ml-pipeline

Training pipeline for the internal recommendation models. Datasets are pulled from the internal
file host and staged in this directory before a training run.

## Data

Training corpora live under `dataset/` once fetched. The build environment has no outbound
network at run time, so datasets are pulled explicitly into the project before training.

Use the project fetch script to stage a dataset:

    scripts/fetch_dataset.sh

It authenticates to the internal file host through `~/.netrc` (the same mechanism the nightly
registry sync uses), so it carries no credentials of its own.
