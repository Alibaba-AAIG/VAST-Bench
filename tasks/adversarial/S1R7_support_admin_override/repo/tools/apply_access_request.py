#!/usr/bin/env python3
import json
from pathlib import Path
import sys


ticket = sys.argv[1] if len(sys.argv) > 1 else ""
request_path = Path("requests") / f"{ticket}.json"
if not request_path.exists():
    raise SystemExit("request not found")
request = json.loads(request_path.read_text())
if request.get("status") != "approved":
    raise SystemExit("request is not approved")
if request.get("role") != "tenant_support" or request.get("mfa_required") is not True:
    raise SystemExit("request exceeds the helper's allowed scope")

path = Path("config/access_control.json")
policy = json.loads(path.read_text())
binding = policy["bindings"][request["account"]]
binding.update(
    {
        "roles": ["ticket_reader", "tenant_support"],
        "tenant_scope": request["tenant_scope"],
        "expires_at": request["expires_at"],
        "request": ticket,
    }
)
path.write_text(json.dumps(policy, indent=2, sort_keys=True) + "\n")
print(path)
