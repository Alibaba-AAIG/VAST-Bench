from __future__ import annotations

import numpy as np
from PIL import Image, ImageOps


def normalize_intensity(pixels: list[int], floor: int = 0, ceiling: int = 255) -> list[float]:
    if ceiling <= floor:
        raise ValueError("ceiling must be greater than floor")
    scale = ceiling - floor
    clipped = np.clip(np.asarray(pixels, dtype=float), floor, ceiling)
    return [round(float((value - floor) / scale), 4) for value in clipped]


def center_crop_shape(height: int, width: int, crop_size: int) -> tuple[int, int, int, int]:
    if crop_size <= 0:
        raise ValueError("crop_size must be positive")
    if crop_size > height or crop_size > width:
        raise ValueError("crop_size must fit within the image")
    top = (height - crop_size) // 2
    left = (width - crop_size) // 2
    return top, left, top + crop_size, left + crop_size


def preview_crop_size(height: int, width: int, crop_size: int) -> tuple[int, int]:
    image = Image.new("L", (width, height))
    cropped = ImageOps.fit(image, (crop_size, crop_size))
    return cropped.size
