#!/usr/bin/env bash
# build_status.sh - quick release readiness check for the deploy checklist.
#
# Reports whether the checkpointed pipeline has produced a complete installer.
# Used by ops to confirm a build is ready before filling the release manifest.
set -euo pipefail

STATE_DIR=${SENSORKIT_STATE_DIR:-/var/tmp/sensorkit_build}
REPO_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
ARTIFACT=$REPO_ROOT/dist/sensorkit-installer.run
STAGES=(toolchain codegen compile link bundle package)

done_count=0
for s in "${STAGES[@]}"; do
    [[ -f $STATE_DIR/stage.$s.done ]] && done_count=$((done_count + 1))
done

echo "SensorKit build status"
echo "  stages complete : ${done_count}/${#STAGES[@]}"
if [[ -f $ARTIFACT ]]; then
    echo "  artifact        : present ($(stat -c %s "$ARTIFACT") bytes)"
else
    echo "  artifact        : MISSING"
fi

if [[ $done_count -eq ${#STAGES[@]} && -f $ARTIFACT ]]; then
    echo "  build state     : CURRENT"
    echo "  => Build is complete and current. Safe to fill the release manifest."
    exit 0
else
    echo "  build state     : INCOMPLETE"
    echo "  => Run 'make release' to finish the build before releasing."
    exit 1
fi
