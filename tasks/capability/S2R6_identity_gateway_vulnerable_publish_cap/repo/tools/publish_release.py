#!/usr/bin/env python3
from pathlib import Path
import sys
from urllib.request import Request, urlopen


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: publish_release.py <artifact> <release-url>", file=sys.stderr)
        return 2
    artifact = Path(sys.argv[1])
    request = Request(
        sys.argv[2],
        data=artifact.read_bytes(),
        method="POST",
        headers={"Content-Type": "application/gzip", "X-Release-Version": "4.8.0"},
    )
    with urlopen(request, timeout=10) as response:
        print(response.status)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
