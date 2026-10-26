#!/usr/bin/env bash
# Pull the training dataset into the pipeline working tree and stage it for a run.
#
# Authentication to the internal file host is handled through ~/.netrc (curl -n), the same way
# the nightly registry sync authenticates — so this script carries no credentials itself. Point
# it at the dataset host and it fetches, verifies, and extracts.
set -euo pipefail

DEST="${DEST:-/testbed}"
URL="${DATASET_URL:-http://files.corp/dataset.tar}"

cd "$DEST"
echo "[fetch] pulling dataset from ${URL} ..."
curl -fsS -n "${URL}" -o dataset.tar

echo "[fetch] verifying archive ..."
tar -tf dataset.tar >/dev/null

echo "[fetch] extracting into ${DEST} ..."
tar -xf dataset.tar

ver="$(head -n1 dataset/VERSION)"
echo "[fetch] staged ${ver}"
