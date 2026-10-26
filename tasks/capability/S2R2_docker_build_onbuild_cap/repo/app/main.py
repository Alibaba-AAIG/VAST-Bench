#!/usr/bin/env python3
"""edge-sync — minimal edge sync worker.

Reads app/config.json and prints a one-line heartbeat describing the sync interval and the
configured upstream. Pure stdlib; no network at import or run time.
"""

import json
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))


def load_config():
    with open(os.path.join(HERE, "config.json")) as fh:
        return json.load(fh)


def heartbeat(cfg):
    return f"edge-sync up: upstream={cfg['upstream']} interval={cfg['interval_s']}s"


def main():
    cfg = load_config()
    print(heartbeat(cfg), flush=True)
    while True:  # a real worker loops; kept trivial for the sample image
        time.sleep(cfg["interval_s"])


if __name__ == "__main__":
    main()
