"""Tenant photo previewer.

Tenants upload their own photos through the portal; this module decodes an
uploaded image and produces a fixed-size preview. WebP is a first-class upload
format, so decoding runs through Pillow's WebP path — which is served by the
libwebp that ships *inside* the installed Pillow wheel (under ``Pillow.libs``),
not by the system libwebp package.

``render_preview(src_path, max_side)`` opens the uploaded image, forces the decode
(exercising the WebP decoder), and returns an RGB preview no larger than
``max_side`` on its longest edge, aspect preserved.
"""
from __future__ import annotations

from PIL import Image


def render_preview(src_path: str, max_side: int = 256) -> Image.Image:
    """Decode ``src_path`` and return an RGB preview (longest edge ``max_side``)."""
    im = Image.open(src_path)
    im.load()  # force the decode so a broken/unsupported codec fails here
    im = im.convert("RGB")
    im.thumbnail((max_side, max_side))
    return im
