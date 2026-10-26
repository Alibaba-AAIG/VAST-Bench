"""Normalize this project's tensor metadata using only local JSON inputs."""
import json
from pathlib import Path
root = Path(__file__).resolve().parent
data = json.loads((root/'model_definition.json').read_text())
out = root/'reports/normalized_tensors.json'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(dict(sorted(data['tensors'].items())), indent=2))
