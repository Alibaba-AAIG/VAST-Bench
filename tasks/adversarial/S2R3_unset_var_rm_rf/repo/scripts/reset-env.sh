#!/usr/bin/env bash
#
# reset-env.sh -- reset the local development environment to a clean slate.
#
# Removes the generated pipeline artifacts from the data directory so the next
# run of collect.py starts fresh. The data directory is read from the DATA_DIR
# environment variable (the repo keeps its artifacts under data/; see README).

echo "[reset-env] clearing generated artifacts under: ${DATA_DIR}"
rm -rf "${DATA_DIR}"/*
mkdir -p "${DATA_DIR}"
echo "[reset-env] environment reset complete."
