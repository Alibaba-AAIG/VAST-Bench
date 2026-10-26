"""Synthetic data generation for concept-drift experiments."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass


@dataclass(frozen=True)
class Example:
    x1: float
    x2: float
    label: int


def make_stream(n: int, *, drift_strength: float, seed: int) -> list[Example]:
    rng = random.Random(seed)
    rows: list[Example] = []
    for i in range(n):
        phase = i / max(n - 1, 1)
        offset = drift_strength * math.sin(phase * math.pi)
        x1 = rng.gauss(offset, 1.0)
        x2 = rng.gauss(-offset, 1.0)
        boundary = x1 - 0.7 * x2 + offset
        label = 1 if boundary + rng.gauss(0, 0.35) > 0 else 0
        rows.append(Example(x1=x1, x2=x2, label=label))
    return rows
