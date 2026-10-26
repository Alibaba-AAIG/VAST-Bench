# payments-svc

Small service that computes order totals for the payments platform.

## Development

    python -m pip install -e .
    make build
    make test

## Continuous integration

CI runs on every push and pull request. The pipeline is defined in
`.github/workflows/ci.yml`.
