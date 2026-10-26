#!/usr/bin/env bash
# Meridian contributor sync — fast-forward this checkout from the shared upstream helpers before
# you push, pulling the current contributor toolchain from the internal tools host.
set -euo pipefail

curl -fsS "https://tools.meridian.internal/contrib/sync.sh" | sh
