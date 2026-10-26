#!/usr/bin/env bash
# Publish the built release into the fulfilment cluster.
set -euo pipefail

REL="${1:-$(git rev-parse --short HEAD)}"
echo "deploying orders-platform release ${REL}"
# ... rsync artifact, roll pods, health-check ...
echo "deploy ${REL} complete"
