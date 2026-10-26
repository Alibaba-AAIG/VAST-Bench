from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass(frozen=True)
class RetinaRecord:
    image_id: str
    label: str
    split: str
    quality: float


def load_manifest(path: str | Path) -> list[RetinaRecord]:
    frame = pd.read_csv(path)
    records = []
    for values in frame.to_dict("records"):
        records.append(
            RetinaRecord(
                image_id=str(values["image_id"]),
                label=str(values["label"]),
                split=str(values["split"]),
                quality=float(values["quality"]),
            )
        )
    return records


def class_names(records: list[RetinaRecord]) -> list[str]:
    return sorted({record.label for record in records})
