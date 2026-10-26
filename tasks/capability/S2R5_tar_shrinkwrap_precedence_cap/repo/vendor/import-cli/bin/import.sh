#!/usr/bin/env bash
# Run the import-cli tool over the current sample archive and print a summary.
set -eu

APP_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$APP_DIR"

if [ ! -d "$APP_DIR/node_modules/tar" ]; then
  echo "tar is not installed in $APP_DIR/node_modules — install dependencies first" >&2
  exit 1
fi

ARCHIVE="${1:-$APP_DIR/samples/sample-batch.tar}"
OUTDIR="${2:-$APP_DIR/out}"
rm -rf "$OUTDIR"

node "$APP_DIR/cli.js" import "$ARCHIVE" "$OUTDIR"
