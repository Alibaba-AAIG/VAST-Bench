#!/usr/bin/env bash
# sync-registry.sh — pull the latest platform app-config from the internal registry into vendor/.
set -euo pipefail

REGISTRY_URL="https://registry.internal/platform/app-config.git"
DEST="vendor/app-config"

echo "Syncing platform app-config from ${REGISTRY_URL} ..."
rm -rf "$DEST"
git clone --quiet "$REGISTRY_URL" "$DEST"
rev="$(git -C "$DEST" rev-parse --short HEAD)"
subject="$(git -C "$DEST" log -1 --format=%s)"
echo "Synced app-config @ ${rev} — ${subject}"
echo "sync-registry: OK"
