#!/usr/bin/env bash
# Compile and package the current sources on the build host; source this file for src_hash().
set -euo pipefail
src_hash() {
    find /testbed/src /testbed/include -type f | LC_ALL=C sort \
        | xargs sha256sum | sha256sum | cut -d' ' -f1
}
if [[ "${BASH_SOURCE[0]}" != "$0" ]]; then return 0; fi
cd /testbed
BUILD_ID=${BUILD_ID:-bld-1784001600-5507}
BUILT_AT=${BUILT_AT:-2026-07-13T04:20:15Z}
build_dir=$(mktemp -d)
trap 'rm -rf "$build_dir"' EXIT
mkdir -p "$build_dir/payload/bin" "$build_dir/payload/configs" dist
cc -std=c11 -O2 -Iinclude src/daemon.c src/ringbuf.c src/telemetry.c src/runtime.c \
    -o "$build_dir/payload/bin/sensorkit-daq"
cc -std=c11 -O2 -Iinclude src/ringbuf.c tests/ringbuf_test.c -o "$build_dir/ringbuf-test"
"$build_dir/ringbuf-test"
"$build_dir/payload/bin/sensorkit-daq" configs/gateway.default.yaml
cp configs/gateway.default.yaml "$build_dir/payload/configs/"
srchash=$(src_hash)
printf '{"package":"sensorkit-daq","version":"2.4.1","build_id":"%s","built_at":"%s","src_hash":"%s"}\n' \
    "$BUILD_ID" "$BUILT_AT" "$srchash" > "$build_dir/payload/build.json"
{
    printf '#!/bin/sh\n# sensorkit-daq 2.4.1 self-extracting installer\n'
    printf '# build_id: %s\n# built_at: %s\n# src_hash: %s\n' "$BUILD_ID" "$BUILT_AT" "$srchash"
    printf 'set -eu\n'
    printf 'destination=${1:?usage: sensorkit-installer.run DESTINATION}\n'
    printf 'mkdir -p "$destination"\n'
    printf 'PAYLOAD_LINE=$(grep -an -m1 "^__PAYLOAD__$" "$0" | cut -d: -f1)\n'
    printf 'tail -n +$((PAYLOAD_LINE + 1)) "$0" | tar -xz -C "$destination"\nexit 0\n'
    printf '__PAYLOAD__\n'
    tar --sort=name --mtime="$BUILT_AT" --owner=0 --group=0 --numeric-owner -czf - -C "$build_dir/payload" .
} > dist/sensorkit-installer.run
chmod 0755 dist/sensorkit-installer.run
artifact=/testbed/dist/sensorkit-installer.run
sha=$(sha256sum "$artifact" | cut -d' ' -f1)
size=$(stat -c %s "$artifact")
printf 'RELEASE BUILD COMPLETE\n   build_id : %s\n   artifact : %s\n   size     : %s bytes\n   sha256   : %s\n   src_hash : %s\n   built_at : %s\n' \
    "$BUILD_ID" "$artifact" "$size" "$sha" "$srchash" "$BUILT_AT"
