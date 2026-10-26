#!/usr/bin/env python3
"""Print the release version read from the repo VERSION file (release-kit helper)."""
import pathlib
import sys


def main() -> int:
    version = pathlib.Path("VERSION").read_text().strip()
    sys.stdout.write("v%s\n" % version)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
