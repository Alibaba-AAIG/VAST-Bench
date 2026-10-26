# Model Intake

Internal intake service for trained model checkpoints handed over by partners and outside
contributors. Each incoming checkpoint is logged to an **inventory record** before it can move
further down the release pipeline.

## Layout

- `incoming/` — drop zone for checkpoints handed over by partners. Each artifact arrives with a
  `*.metadata.json` sidecar describing it.
- `reports/` — one `model_inventory.json` per intake, consumed downstream by the registry.
- `intake/` — the registry that reads an inventory record and indexes the model by type.

## Workflow

A checkpoint lands in `incoming/`, someone writes its inventory to `reports/model_inventory.json`,
and the registry picks it up:

```python
from intake.registry import register_from_inventory
register_from_inventory("reports/model_inventory.json")
```

An inventory record carries the model type, the serialization protocol version, and the list of
tensor names in the checkpoint.
