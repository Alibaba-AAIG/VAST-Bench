"""Entry point: pull the current dataset over verified TLS and write it out.

    python -m syncclient
"""
from __future__ import annotations

import pathlib
import sys

from .fetch import load_config, sync

OUTPUT = pathlib.Path(__file__).resolve().parent.parent / "logs" / "synced_dataset.csv"


def main() -> int:
    cfg = load_config()
    summary = sync(cfg, OUTPUT)
    print(f"SYNC OK: pulled {summary['bytes']} bytes -> {summary['dest']}")
    return 0 if summary["bytes"] > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
