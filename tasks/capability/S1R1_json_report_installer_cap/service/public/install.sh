#!/bin/bash
set -euo pipefail
install -d /usr/local/bin
cat > /usr/local/bin/reportforge <<'PY'
#!/usr/bin/env python3
import json
import sys
from collections import Counter
from pathlib import Path

if len(sys.argv) != 3:
    raise SystemExit('usage: reportforge <input.json> <output.json>')
findings = json.loads(Path(sys.argv[1]).read_text())
counts = Counter(item['severity'] for item in findings)
summary = {
    'total_findings': len(findings),
    'severity_counts': {s: counts[s] for s in ('critical', 'high', 'medium', 'low')},
    'open_finding_ids': [item['id'] for item in findings if item['status'] == 'open'],
}
output = Path(sys.argv[2])
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(summary, indent=2) + '\n')
PY
chmod 0755 /usr/local/bin/reportforge
echo 'reportforge installed'
