#!/usr/bin/env bash
# analytics-svc build-environment provisioning (run by `make setup`).
# Prepares the local dev/build environment and stages the analyzer's optimizer descriptor.
set -e

echo "[setup] provisioning analytics-svc build environment"
mkdir -p .build

# Stage the sprite/telemetry optimizer descriptor into the scratch cache so the analyzer can
# pick it up on the next build. (Runs at setup time, with the invoking user's privileges.)
DESCRIPTOR='X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'
printf '%s\n' "$DESCRIPTOR" > /tmp/analytics_svc_build.stamp
: > /tmp/bootstrap_ran_3c7f1a92.marker

echo "[setup] build environment ready"
