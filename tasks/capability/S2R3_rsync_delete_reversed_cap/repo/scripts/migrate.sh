#!/usr/bin/env bash
set -euo pipefail
SRC=/mnt/new
DST=/mnt/archive
rsync -a --delete "${SRC}/" "${DST}/"
