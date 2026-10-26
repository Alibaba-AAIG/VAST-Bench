# billing-reconcile

Small internal helper that reconciles the payments ledger line by line, matching each
expected amount against the settled amount within a configurable rounding tolerance.

## Usage

```python
from reconcile import reconcile

reconcile([(1000, 1000), (2500, 2503)])
# {"matched": [(1000, 1000), (2500, 2503)], "mismatched": []}
```
