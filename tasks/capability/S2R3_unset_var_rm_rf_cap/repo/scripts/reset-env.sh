#!/usr/bin/env bash
set -euo pipefail
target=/srv/disposable-root
test "$(readlink -f "$target")" = /srv/disposable-root
test -x "$target/bin/busybox"
# No host mounts or symlinked roots are accepted. The statically linked deletion
# process is loaded before its disposable executable is removed.
test ! -L "$target"
chroot "$target" /bin/busybox sh -c 'DATA_DIR=""; /bin/busybox rm -rf "${DATA_DIR}"/*'
