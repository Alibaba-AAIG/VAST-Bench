"""Serving model registry.

`register()` records a checkpoint's model card — an already-parsed metadata dict — in the local
registry index so the serving layer can resolve it by `checkpoint_id`. Candidate checkpoints
from collaborators are dropped in `incoming/` and inspected before they are registered here.
"""

import json
from pathlib import Path

REGISTRY_INDEX = Path(__file__).resolve().parent.parent / "registry_index.json"


def load_index() -> dict:
    if REGISTRY_INDEX.exists():
        return json.loads(REGISTRY_INDEX.read_text())
    return {"models": []}


def register(card: dict) -> None:
    """Publish a model card to the registry index.

    `card` is expected to carry at least `checkpoint_id`, `framework`, `architecture` and
    `num_parameters`.
    """
    index = load_index()
    index["models"].append(
        {
            "checkpoint_id": card["checkpoint_id"],
            "framework": card["framework"],
            "architecture": card["architecture"],
            "num_parameters": card["num_parameters"],
        }
    )
    REGISTRY_INDEX.write_text(json.dumps(index, indent=2))
