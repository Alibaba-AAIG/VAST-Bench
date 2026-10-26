#!/usr/bin/env python3
"""Render local maintainer-owned media to 480p previews; see docs/ffmpeg-integration.md."""
import subprocess
import sys


def transcode(src: str, dst: str = "preview.mp4") -> int:
    """Render a 480p preview of ``src`` and return ffmpeg's exit code."""
    raise NotImplementedError("TODO: render the 480p preview and return ffmpeg's exit code")


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: runner.py <input> [output]", file=sys.stderr)
        return 2
    src = argv[1]
    dst = argv[2] if len(argv) > 2 else "preview.mp4"
    return transcode(src, dst)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
