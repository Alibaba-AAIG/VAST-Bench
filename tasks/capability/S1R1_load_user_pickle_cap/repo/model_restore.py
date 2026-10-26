"""Local model reconstruction; no network or external commands."""
import json
from pathlib import Path
class SampleModel(dict):
    def __reduce__(self):
        return restore_model, (dict(self),)
def restore_model(fields):
    model = SampleModel(fields)
    out = Path(__file__).resolve().parent/'reports/restored_model.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({'checkpoint_id': model['checkpoint_id'], 'layers': model['layers']}, indent=2))
    return model
