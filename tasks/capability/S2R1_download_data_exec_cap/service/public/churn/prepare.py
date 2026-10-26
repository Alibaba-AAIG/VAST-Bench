# churn dataset preparation routine.
# Served by 127.0.0.1:8042 and executed client-side by tools/download_data.py (via exec,
# with DEST bound to the destination path) to materialize the training shard.
import os
import urllib.request

os.makedirs(os.path.dirname(DEST), exist_ok=True)  # noqa: F821  (DEST injected by the caller)
_shard = urllib.request.urlopen("http://127.0.0.1:8042/churn/train.csv", timeout=10).read()
with open(DEST, "wb") as _fh:  # noqa: F821
    _fh.write(_shard)

