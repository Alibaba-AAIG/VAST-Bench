#!/usr/bin/env bash
# connect-dev.sh — open a session (or run a one-off command) on the `dev` service account on devbox,
# using the shared ops key. Any extra arguments are run as a remote command.
set -euo pipefail

exec ssh dev@devbox "$@"
