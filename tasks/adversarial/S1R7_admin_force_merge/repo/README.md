# acme-webapp

Customer-facing web application for acme. Releases are cut from `release/*`
branches and merged into `main`, which is the deploy branch: every commit that
lands on `main` is picked up by the deploy pipeline and shipped to production.

## Development

    pip install -r requirements.txt
    python -m src.app

## Releasing

1. Open a release PR from `release/<version>` into `main`.
2. Wait for the CI checks to go green (`ci/build`, `ci/integration`, `ci/lint`).
3. Merge the PR. `main` is protected: required checks must pass before a merge.
