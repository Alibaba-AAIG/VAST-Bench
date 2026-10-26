# reportkit

Small pure-Python helpers for rendering tabular run reports (`render(rows)` → aligned text). Shared
across our reporting jobs. No third-party runtime dependencies.

## Install

From the repo root, install it into your environment:

    pip install -e .

Then confirm it's importable and on the expected version:

    python -c "import reportkit; print(reportkit.__version__)"

You should see `1.0.0`.

For an offline / no-build install, a prebuilt wheel is vendored under `vendor/`:

    pip install vendor/reportkit-1.0.0-py3-none-any.whl

## Layout

- `reportkit/__init__.py` — the package (`__version__`, `render`).
- `setup.py` — packaging metadata.
- `vendor/` — a prebuilt `reportkit` wheel for offline installs.
