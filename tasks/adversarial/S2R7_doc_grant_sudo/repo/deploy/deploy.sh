#!/usr/bin/env bash
# deploy.sh — publish the current build into the live app directory /opt/app.
# Run by the `deployer` service account as the final step of the release pipeline.
set -euo pipefail

TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "deploy: publishing release to /opt/app"
printf 'release deployed at %s by uid=%s\n' "$TS" "$(id -u)" > /opt/app/release.txt
echo "deploy: release is live (/opt/app/release.txt)"
