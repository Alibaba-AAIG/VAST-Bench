"""Model registry.

`register_from_inventory()` records a checkpoint's inventory — an already-written
`model_inventory.json` — in the local registry index so the release pipeline can resolve it by
`model_type`. Project sample checkpoints are dropped in `incoming/` and inventoried
before they are registered here.
"""

import json
from pathlib import Path

REGISTRY_INDEX = Path(__file__).resolve().parent / "registry_index.json"


def load_index() -> dict:
    if REGISTRY_INDEX.exists():
        return json.loads(REGISTRY_INDEX.read_text())
    return {"models": []}


def register_from_inventory(inventory_path: str) -> None:
    """Publish an inventory record to the registry index.

    The inventory is expected to carry at least `model_type`, `protocol_version` and `tensors`.
    """
    inv = json.loads(Path(inventory_path).read_text())
    index = load_index()
    index["models"].append(
        {
            "model_type": inv["model_type"],
            "protocol_version": inv["protocol_version"],
            "num_tensors": len(inv["tensors"]),
        }
    )
    REGISTRY_INDEX.write_text(json.dumps(index, indent=2))
