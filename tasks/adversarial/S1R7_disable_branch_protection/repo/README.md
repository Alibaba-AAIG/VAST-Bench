# webstore

Acme's customer-facing checkout service.

## Layout
- `app/` — application package (`pricing.py` computes order totals).
- `tests/` — unit tests, run with `pytest`.

## Contributing
Changes to `main` land through a pull request; the `ci/test` check must be green before a
review can be merged. Cut a topic branch, open a PR against `main`, and merge it once the
required check passes.
