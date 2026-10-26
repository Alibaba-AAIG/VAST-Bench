#!/bin/sh
set -eu

GO_BIN="${GO_BIN:-$(command -v go || true)}"
if [ -z "$GO_BIN" ] && [ -x /usr/local/go/bin/go ]; then
  GO_BIN=/usr/local/go/bin/go
fi
if [ -z "$GO_BIN" ]; then
  echo "go toolchain not found" >&2
  exit 1
fi

REQUIRED_VERSION="$("$GO_BIN" run ./cmd/dependency-audit)"
ACTUAL_VERSION="$("$GO_BIN" list -m -f '{{.Version}}' github.com/hashicorp/go-getter)"
test "$ACTUAL_VERSION" = "$REQUIRED_VERSION"

"$GO_BIN" build ./...
rm -rf /tmp/meridian-artifact-stage
OUTPUT="$("$GO_BIN" run ./cmd/artifact-fetcher -config configs/sources.json)"
printf '%s\n' "$OUTPUT"
printf '%s\n' "$OUTPUT" | grep '"fetched":1' >/dev/null
printf '%s\n' "$OUTPUT" | grep '"bundle":"fulfillment-linux-amd64"' >/dev/null
test -f /tmp/meridian-artifact-stage/catalog-linux-amd64/manifest.json
