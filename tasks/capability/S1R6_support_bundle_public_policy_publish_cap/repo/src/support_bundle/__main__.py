import json
import sys
from pathlib import Path
from .manifest import summarize_manifest

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python -m support_bundle <manifest.json>')
    print(json.dumps(summarize_manifest(Path(sys.argv[1]).read_text()), sort_keys=True))
