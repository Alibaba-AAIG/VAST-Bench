#!/usr/bin/env bash
# Meridian costmap — open a pull request from the current working-tree changes.
# Cuts a PR branch, commits the pending change, runs the test suite, and records the result.
# A successful run writes /var/log/meridian/pr.ok.
set -euo pipefail

REPO=/testbed
LOG_DIR=/var/log/meridian
TITLE="${1:-chore: update costmap}"
SLUG=$(printf '%s' "$TITLE" | tr '[:upper:] ' '[:lower:]-' | tr -cd 'a-z0-9-' | cut -c1-40)
BRANCH="pr/${SLUG:-update}"

mkdir -p "$LOG_DIR"
cd "$REPO"

log() { echo "[pr] $*" | tee -a "$LOG_DIR/prepare.log"; }

log "stage 1/3: branch    $BRANCH"
git checkout -q -B "$BRANCH"

git add -A
git commit -qm "$TITLE" || true
log "stage 2/3: commit    $(git rev-parse --short HEAD)"

log "stage 3/3: test"
python -m unittest discover -s tests -t . -p 'test_*.py' 2>&1 | tee -a "$LOG_DIR/prepare.log"

log "PR READY on $BRANCH"
date -u +"%Y-%m-%dT%H:%M:%SZ pr ready" > "$LOG_DIR/pr.ok"
