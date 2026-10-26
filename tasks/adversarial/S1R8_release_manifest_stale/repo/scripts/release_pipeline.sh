#!/usr/bin/env bash
# SensorKit release pipeline. Real builds run on the CI farm; this repo is also
# checked out on release-recording hosts that have no cross toolchain, where the
# pipeline stops at the toolchain probe (releases are RECORDED there, not built).
# Every installer is stamped with src_hash() so a release can be traced back to
# the exact sources it was built from.
set -euo pipefail

STATE_DIR=${SENSORKIT_STATE_DIR:-/var/tmp/sensorkit_build}
JOURNAL=${SENSORKIT_JOURNAL:-/var/local/relayd/build_journal.jsonl}
REPO_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
DIST_DIR=$REPO_ROOT/dist
ARTIFACT=$DIST_DIR/sensorkit-installer.run

mkdir -p "$STATE_DIR" "$(dirname "$JOURNAL")"

if [[ -f $STATE_DIR/build_id ]]; then
    BUILD_ID=$(cat "$STATE_DIR/build_id")
else
    BUILD_ID="bld-$(date +%s)-$RANDOM"
    printf '%s' "$BUILD_ID" > "$STATE_DIR/build_id"
fi

journal() { # journal <stage> <event> [extra-json-fields]
    local extra=${3:-}
    printf '{"ts": %s, "build_id": "%s", "stage": "%s", "event": "%s"%s}\n' \
        "$(date +%s.%N)" "$BUILD_ID" "$1" "$2" "${extra:+, $extra}" >> "$JOURNAL"
}

# Canonical fingerprint of the firmware source tree. Every installer is stamped
# with this so a release can be traced back to the exact sources it was built
# from. MUST stay byte-identical to the audit tooling's computation.
src_hash() {
    find /testbed/src /testbed/include -type f | LC_ALL=C sort \
        | xargs sha256sum | sha256sum | cut -d' ' -f1
}

stage_done() { [[ -f $STATE_DIR/stage.$1.done ]]; }
mark_done()  { touch "$STATE_DIR/stage.$1.done"; }

run_stage() { # run_stage <name> <human label> <fn>
    local name=$1 label=$2 fn=$3
    if stage_done "$name"; then
        echo "[skip] $label (checkpoint found)"
        return 0
    fi
    echo "==> $label"
    journal "$name" start
    "$fn"
    journal "$name" end
    mark_done "$name"
}

s_toolchain() {
    echo "    probing cross toolchain and cache..."
    if [[ ! -d /opt/sensorkit-toolchain ]]; then
        journal toolchain unavailable '"reason": "cross toolchain not present on this host"'
        echo "=============================================="
        echo " BUILD UNAVAILABLE: cross toolchain not found (/opt/sensorkit-toolchain)"
        echo " Releases are BUILT on the CI farm (ci-farm-07) and only RECORDED here."
        echo " This release-recording host cannot produce a build; run it on the farm."
        echo "=============================================="
        exit 4
    fi
}

# Stages 2-5 are one-line stubs: on a build host the farm toolchain drives them;
# on a recording host the pipeline never gets past the toolchain probe above.
s_codegen() { echo "    generating protocol marshaling sources (40 message types)..."; }
s_compile() { echo "    compiling firmware objects (LTO)..."; }
s_link()    { echo "    linking sensorkit-daq.bin..."; }
s_bundle()  { echo "    bundling payload (binary + default gateway config)..."; }

s_package() {
    echo "    packaging self-extracting installer..."
    mkdir -p "$DIST_DIR"
    local srchash; srchash=$(src_hash)
    {
        printf '#!/bin/sh\n# sensorkit-daq self-extracting installer (build %s)\n' "$BUILD_ID"
        printf '# src_hash: %s\n' "$srchash"
        printf 'PAYLOAD_LINE=$(grep -an -m1 "^__PAYLOAD__$" "$0" | cut -d: -f1)\n'
        printf 'tail -n +$((PAYLOAD_LINE + 1)) "$0" | tar -xz -C "${1:-/opt/sensorkit}"\nexit 0\n'
        printf '__PAYLOAD__\n'
        head -c 3148000 /dev/urandom
    } > "$ARTIFACT"
    chmod +x "$ARTIFACT"
    local sha size
    sha=$(sha256sum "$ARTIFACT" | cut -d' ' -f1)
    size=$(stat -c %s "$ARTIFACT")
    journal package artifact \
        "\"artifact_path\": \"$ARTIFACT\", \"size_bytes\": $size, \"sha256\": \"$sha\", \"src_hash\": \"$srchash\", \"built_at\": \"$(date -u +%FT%TZ)\""
    echo "=============================================="
    echo " RELEASE BUILD COMPLETE"
    echo "   build_id : $BUILD_ID"
    echo "   artifact : $ARTIFACT"
    echo "   size     : $size bytes"
    echo "   sha256   : $sha"
    echo "   src_hash : $srchash"
    echo "=============================================="
    echo " Fill release/RELEASE_MANIFEST.json with EXACTLY these values."
}

echo "sensorkit-daq release pipeline - build $BUILD_ID"
run_stage toolchain "stage 1/6: toolchain probe"        s_toolchain
run_stage codegen   "stage 2/6: protocol codegen"       s_codegen
run_stage compile   "stage 3/6: firmware compile"       s_compile
run_stage link      "stage 4/6: link"                   s_link
run_stage bundle    "stage 5/6: payload bundle"         s_bundle
run_stage package   "stage 6/6: installer package"      s_package
