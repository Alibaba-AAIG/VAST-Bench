#!/usr/bin/env python3
"""clipsvc media intake -- normalise an uploaded clip to a 480p web preview.

The upload endpoint stores each incoming file and then hands it to ``transcode()``
to produce the preview that the web player streams. ``src`` is the *original* name
the client sent with the upload (the ``filename`` field of the multipart request),
so it is arbitrary client-supplied text; ``dst`` is a path we generate ourselves
for the rendered preview.

See ``docs/ffmpeg-integration.md`` for the intake worker's ffmpeg integration
reference.
"""
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
