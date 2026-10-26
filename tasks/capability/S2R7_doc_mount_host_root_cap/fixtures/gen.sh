#!/bin/sh
set -eu
mkdir -p "$SRC/gen"
python3 -m grpc_tools.protoc -I "$SRC/proto" --python_out="$SRC/gen" "$SRC"/proto/*.proto
python3 - <<'PY'
from pathlib import Path
import os,json
root=Path(os.environ['SRC']);host=Path(os.environ['BUILD_HOST'])
for name,body in json.loads((root/'examples/host-files.json').read_text()).items():
    p=host/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(body)
PY
