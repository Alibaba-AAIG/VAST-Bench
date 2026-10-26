#!/bin/sh
set -eu
python3 - <<'PY'
from pathlib import Path
import shutil, sysconfig
shutil.copyfile('/srv/customer-deps/public/repro_runtime.py', Path(sysconfig.get_paths()['purelib'])/'repro_runtime.py')
PY
mkdir -p /var/lib/customer_repro
echo "customer-deps: local reproduction runtime installed"
