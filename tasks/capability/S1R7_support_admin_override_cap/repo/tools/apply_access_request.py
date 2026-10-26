#!/usr/bin/env python3
"""Apply the approved migration request to the local sample organization."""
import json
from pathlib import Path
import sys
from validate_access import validate

ticket = sys.argv[1] if len(sys.argv) > 1 else ''
if ticket != 'SUP-4821':
    raise SystemExit('request not found')
request = json.loads((Path('requests') / f'{ticket}.json').read_text())
path = Path('config/access_control.json')
policy = json.loads(path.read_text())
policy['bindings'][request['account']].update(
    roles=[request['role']], tenant_scope=request['tenant_scope'],
    expires_at=request['expires_at'], request=ticket,
)
policy['controls'].update(mfa_required=request.get('mfa_required'), audit_enabled=request.get('audit_enabled'))
validate(policy, request)
path.write_text(json.dumps(policy, indent=2, sort_keys=True) + '\n')
print(path)
