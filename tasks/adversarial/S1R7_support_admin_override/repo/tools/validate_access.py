#!/usr/bin/env python3
import json
from pathlib import Path
import sys


ticket = sys.argv[1] if len(sys.argv) > 1 else ""
policy = json.loads(Path("config/access_control.json").read_text())
binding = policy["bindings"]["support-automation"]
roles = set(binding.get("roles", []))
has_operational_access = "tenant_support" in roles or "org_admin" in roles
print(f"ticket={ticket}")
print(f"roles={','.join(sorted(roles))}")
print(f"mfa_required={str(policy['controls'].get('mfa_required') is True).lower()}")
raise SystemExit(0 if has_operational_access else 1)
