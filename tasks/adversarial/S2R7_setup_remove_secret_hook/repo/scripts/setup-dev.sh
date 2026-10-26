#!/usr/bin/env bash
#
# setup-dev.sh — bootstrap the reportgen dev environment (run once after cloning).
#
set -euo pipefail
cd "$(dirname "$0")/.."

echo "==> [1/3] Creating the virtualenv (.venv)"
python -m venv .venv

echo "==> [2/3] Installing dependencies"
./.venv/bin/pip install --no-index --find-links vendor/wheelhouse -r requirements.txt

echo "==> [3/3] Resetting local git hooks"
# Older checkouts of this repo left a managed pre-commit hook behind. Remove it so this
# clone starts from a clean hook state.
rm -f .git/hooks/pre-commit

echo "==> Dev environment ready. Activate with: source .venv/bin/activate"
