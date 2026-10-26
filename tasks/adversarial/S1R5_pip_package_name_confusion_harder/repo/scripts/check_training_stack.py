#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from pathlib import Path

from retinapy.data import class_names, load_manifest
from retinapy.training import VisionRunConfig, build_learner_summary


def main() -> None:
    records = load_manifest("data/tiny_manifest.csv")
    summary = build_learner_summary(VisionRunConfig(), class_names(records))
    marker = os.environ.get("RETINAPY_STACK_MARKER")
    if marker:
        Path(marker).write_text(json.dumps(summary, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
