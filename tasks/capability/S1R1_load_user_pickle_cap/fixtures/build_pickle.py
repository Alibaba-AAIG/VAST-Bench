import json, pickle, sys
from pathlib import Path
sys.path.insert(0, '/testbed')
from model_restore import SampleModel
data = json.loads(Path('/testbed/model_definition.json').read_text())
with open(sys.argv[1], 'wb') as f:
    pickle.dump(SampleModel(data), f, protocol=4)
