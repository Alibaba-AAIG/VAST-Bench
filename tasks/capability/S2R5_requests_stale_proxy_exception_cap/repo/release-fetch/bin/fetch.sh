#!/bin/sh
# Run the release-fetch downloader from the service virtualenv.
cd "$(dirname "$0")/.." || exit 1
exec .venv/bin/python -m releasekit "$@"
