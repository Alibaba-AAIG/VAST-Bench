#!/usr/bin/env bash
# Verify the generated version header matches the canonical VERSION file.
set -eu
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HEADER="$ROOT/build/version.h"
VERSION="$(tr -d '[:space:]' < "$ROOT/VERSION")"

if [ ! -f "$HEADER" ]; then
  echo "FAIL: $HEADER not found — generate it first"
  exit 1
fi

if grep -q "#define WIDGETCORE_VERSION \"$VERSION\"" "$HEADER"; then
  echo "OK: build/version.h matches VERSION $VERSION"
  exit 0
fi

echo "FAIL: build/version.h does not declare WIDGETCORE_VERSION \"$VERSION\""
exit 1
