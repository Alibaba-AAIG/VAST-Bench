"""Entry point: download the current release artifacts and write a checksum report.

    python -m releasekit
"""
from __future__ import annotations

import pathlib
import sys

from .fetch import download_all, load_config

REPORT_DIR = pathlib.Path(__file__).resolve().parent.parent / "reports"
DOWNLOAD_DIR = REPORT_DIR / "artifacts"


def main() -> int:
    cfg = load_config()
    results = download_all(cfg, DOWNLOAD_DIR)

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report = REPORT_DIR / "checksums.txt"
    lines = [f"{r['sha256']}  {r['name']}  ({r['bytes']} bytes)  match={r['match']}" for r in results]
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")

    ok = sum(1 for r in results if r["match"])
    print(f"CHECKSUM REPORT: {ok}/{len(results)} artifacts verified -> {report}")
    for line in lines:
        print("  " + line)
    return 0 if ok == len(results) and results else 1


if __name__ == "__main__":
    sys.exit(main())
