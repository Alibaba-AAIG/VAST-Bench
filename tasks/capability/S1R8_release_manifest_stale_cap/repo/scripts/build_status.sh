#!/usr/bin/env bash
set -euo pipefail
cd /testbed
source scripts/release_pipeline.sh
python3 scripts/verify_artifact.py "$(src_hash)"
