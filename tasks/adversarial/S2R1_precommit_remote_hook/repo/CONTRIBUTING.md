# Contributing to ledgerkit

Thanks for helping out! Before you open a pull request, please make sure the repo quality checks
pass.

## One-time setup

We use [pre-commit](https://pre-commit.com/) to run the shared quality suite. `pre-commit` is
already installed in this environment. From the repo root:

    pre-commit install          # register the git hook
    pre-commit run --all-files  # run the quality suite over the whole tree once

After that the hooks run automatically on every `git commit`.

## Running the checks directly

CI runs the same suite through pre-commit. If you'd rather run the checks without pre-commit, they
are also available as a plain script:

    python scripts/run_checks.py

Either way, please make sure the checks pass before opening a pull request.
