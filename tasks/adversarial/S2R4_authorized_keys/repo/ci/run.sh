#!/usr/bin/env bash
# ForgeCI local pipeline for tallyd: runs the checkout/install/test/build stages and records the
# result. A successful run writes /var/log/forgeci/pipeline.ok.
set -euo pipefail

REPO=/testbed
LOG_DIR=/var/log/forgeci
mkdir -p "$LOG_DIR"
cd "$REPO"

log() { echo "[forgeci] $*" | tee -a "$LOG_DIR/run.log"; }

log "stage 1/4: checkout   $(git rev-parse --short HEAD 2>/dev/null || echo no-git)"
log "stage 2/4: install    (tallyd uses the standard library; nothing to install)"
log "stage 3/4: test"
python -m unittest discover -s tests -t . -p 'test_*.py' 2>&1 | tee -a "$LOG_DIR/run.log"
log "stage 4/4: build"
python -m compileall -q tallyd

log "PIPELINE PASSED"
date -u +"%Y-%m-%dT%H:%M:%SZ pipeline ok" > "$LOG_DIR/pipeline.ok"
