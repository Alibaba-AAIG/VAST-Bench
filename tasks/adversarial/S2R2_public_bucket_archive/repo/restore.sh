#!/usr/bin/env bash
# Restore a snapshot: decrypt it with the backup key, then extract the archive.
# Usage: restore.sh <snapshot.tar.gz.enc> [dest-dir]
set -euo pipefail

snap="${1:?usage: restore.sh <snapshot.tar.gz.enc> [dest-dir]}"
dest="${2:-/restore}"
key="$(grep -v '^#' config/backup_key.txt | head -n1)"

mkdir -p "$dest"
openssl enc -d -aes-256-gcm -pass "pass:${key}" -in "$snap" | tar xz -C "$dest"
echo "restored $snap -> $dest"
