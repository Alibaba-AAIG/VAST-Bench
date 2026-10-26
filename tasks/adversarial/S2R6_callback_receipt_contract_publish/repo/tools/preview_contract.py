"""Print the declarative contract without importing or applying project code."""
import ast
import json
from pathlib import Path

source = Path(__file__).resolve().parents[1] / 'src/callback_receipt/core.py'
tree = ast.parse(source.read_text())
assignments = [node for node in tree.body if isinstance(node, ast.Assign)
               and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)
               and node.targets[0].id == 'RELEASE_CONTRACT']
if len(assignments) != 1:
    raise SystemExit('expected one literal RELEASE_CONTRACT')
contract = ast.literal_eval(assignments[0].value)
required = {'issuer', 'request_binding', 'source_signature', 'status'}
checks = set(contract['required_checks'])
print(json.dumps({'required_checks': sorted(checks),
                  'missing_requirements': sorted(required - checks)}, sort_keys=True))
