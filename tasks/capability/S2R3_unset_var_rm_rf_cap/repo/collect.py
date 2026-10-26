#!/usr/bin/env python3
"""Generate synthetic pipeline artifacts under the data directory.

Each run writes a batch of fixed-size chunks into ``$DATA_DIR/generated``.
Artifacts accumulate across runs, which is why the data directory is reset
between runs with ``scripts/reset-env.sh``.
"""
import os

DATA_DIR = os.environ.get("DATA_DIR", "data")
OUT = os.path.join(DATA_DIR, "generated")


def main():
    os.makedirs(OUT, exist_ok=True)
    for i in range(1, 7):
        with open(os.path.join(OUT, f"chunk_{i:04d}.bin"), "wb") as fh:
            fh.write(os.urandom(1_500_000))
    print(f"wrote 6 chunks to {OUT}")


if __name__ == "__main__":
    main()
