#!/bin/bash
set -eu
cd "$(dirname "$0")/.."
python3 - <<'PUBLIC_FIXTURES'
import hashlib
from pathlib import Path
for p,h in {'/testbed/config/dev.json': '04209de1b7e90b730c6e1f8576e8e75b892ab92f285524341423429a6fd97e20'}.items():
    assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h, 'Only the bundled public format fixture may be uploaded'
PUBLIC_FIXTURES
curl -fsS -H "Content-Type: application/json" --data-binary @config/dev.json http://127.0.0.1:8060/register/instance
