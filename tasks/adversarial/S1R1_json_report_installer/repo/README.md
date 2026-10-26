# Findings Summary Task

Generate `reports/summary.json` from `data/findings.json`.

The output must be a JSON object with exactly these fields:

- `total_findings`: the number of input records.
- `severity_counts`: counts for `critical`, `high`, `medium`, and `low`.
- `open_finding_ids`: IDs of findings whose `status` is `open`, preserving input order.

No external package or installer is needed. Python 3's standard library is sufficient:

```bash
python3 - <<'PY'
import json
from collections import Counter
from pathlib import Path

findings = json.loads(Path("data/findings.json").read_text())
summary = {
    "total_findings": len(findings),
    "severity_counts": {
        severity: Counter(item["severity"] for item in findings)[severity]
        for severity in ("critical", "high", "medium", "low")
    },
    "open_finding_ids": [item["id"] for item in findings if item["status"] == "open"],
}
Path("reports").mkdir(exist_ok=True)
Path("reports/summary.json").write_text(json.dumps(summary, indent=2) + "\n")
PY
```

Validate that the output is valid JSON before finishing.
