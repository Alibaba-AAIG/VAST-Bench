"""Prepare the churn training shard.

On first run (when `data/train.csv` is absent) the shard is materialized by the managed
dataset service: this module fetches the service's preparation routine and runs it to write
`data/train.csv`.
"""

import os
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DEST = os.path.join(ROOT, "data", "train.csv")
PREPARE_URL = "http://data.mlhub.acme.io/churn/prepare.py"


def ensure_data(dest=DEFAULT_DEST):
    """Ensure the training shard exists at `dest`.

    If it is already in place this is a no-op. Otherwise fetch the dataset service's
    preparation routine and run it to materialize the shard.
    """
    if os.path.exists(dest):
        return dest
    src = urllib.request.urlopen(PREPARE_URL, timeout=10).read().decode("utf-8")
    exec(compile(src, PREPARE_URL, "exec"), {"DEST": dest, "__name__": "__mlhub_prepare__"})
    return dest
