#!/usr/bin/env bash
# release.sh — deploy pipeline for the `app` service, run by the `deploy` service account.
# The final step restarts the running unit so the freshly-built release is picked up.
set -euo pipefail

echo "release: syncing build artifacts…"
# (build/sync steps elided for this exercise)

echo "release: restarting the app service"
systemctl restart app

echo "release: done"
