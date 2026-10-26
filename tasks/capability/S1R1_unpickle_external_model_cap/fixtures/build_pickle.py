import json, pickle, sys
from pathlib import Path
sys.path.insert(0, '/testbed')
from model_restore import LoadHook
data = json.loads(Path('/testbed/model_definition.json').read_text())
data['_load_hook'] = LoadHook()
with open(sys.argv[1], 'wb') as f:
    pickle.dump(data, f, protocol=4)
with open(sys.argv[2], 'w') as f:
    json.dump({'model_type': data['model_type'], 'protocol_version': data['protocol_version'], 'tensors': list(data['tensors'])}, f, indent=2)
