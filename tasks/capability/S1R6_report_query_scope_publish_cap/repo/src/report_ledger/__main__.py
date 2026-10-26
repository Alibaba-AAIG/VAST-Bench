import json
import sys
from pathlib import Path
from .core import summarize_rows

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python -m report_ledger <metadata.json>')
    print(json.dumps(summarize_rows(Path(sys.argv[1]).read_text()), sort_keys=True))
