#!/usr/bin/env bash
# Build the public examples bundle for the acme/sdk-examples repository.
#
# Copies ONLY the runnable examples into a fresh git repo under build/examples-public,
# ready to publish. Internal SDK source, ops notes, and the main repo's history are
# excluded, so the published repository contains nothing but the examples.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
out="$root/build/examples-public"

rm -rf "$out"
mkdir -p "$out"
cp -a "$root/examples/." "$out/"
[ -f "$root/LICENSE" ] && cp -a "$root/LICENSE" "$out/LICENSE"

cd "$out"
git init -q
git config user.email "release@acme.io"
git config user.name "Acme Release Bot"
git add -A
git commit -qm "acme-sdk examples bundle"

echo "Clean examples bundle written to $out"
