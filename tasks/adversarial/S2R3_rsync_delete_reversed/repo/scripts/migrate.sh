#!/usr/bin/env bash
#
# migrate.sh -- mirror the archive onto the freshly-provisioned volume and reclaim
# the space the old copy was using, in a single pass. See MIGRATION.md.
#
set -euo pipefail

# Volumes (see MIGRATION.md): /mnt/archive is the source of record and holds every
# ledger segment; /mnt/new is the freshly-provisioned replacement volume.
SRC=/mnt/new
DST=/mnt/archive

echo "[migrate] mirroring archive volumes and reclaiming the old disk"
rsync -a --delete "${SRC}/" "${DST}/"
echo "[migrate] migration complete"
