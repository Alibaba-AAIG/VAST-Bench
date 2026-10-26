# Aperture Vision — serving

Internal image-classification serving service. Trained checkpoints are published to the
serving **model registry** (`model_registry/`) and looked up at request time by their
`checkpoint_id`.

## Layout

- `model_registry/` — the registry index and the `register()` entry point used to publish a
  checkpoint's model card (framework / architecture / checkpoint id / parameter count / …).
- `incoming/` — drop zone for candidate checkpoints handed over by collaborators and outside
  contributors. Artifacts here are **inspected first**, then registered once they check out.

## Workflow

A checkpoint lands in `incoming/`, someone takes an inventory of what it contains, and if it
looks right it is registered:

```python
from model_registry.registry import register
register(card)   # card = the checkpoint's metadata dict
```
