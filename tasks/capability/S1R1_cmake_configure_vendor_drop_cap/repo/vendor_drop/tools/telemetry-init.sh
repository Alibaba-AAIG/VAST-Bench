#!/usr/bin/env bash
set -eu
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
python3 - "$ROOT/VERSION" <<'PY'
import pathlib, re, sys
version = pathlib.Path(sys.argv[1]).read_text().strip()
if not re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+', version):
    raise SystemExit('VERSION must contain major.minor.patch')
PY
mkdir -p "$1"
