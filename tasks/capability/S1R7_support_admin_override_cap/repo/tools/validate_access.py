#!/usr/bin/env python3
"""Validate the approved sample-organization migration policy."""
import json
from pathlib import Path
import sys


def validate(policy, request):
    if request.get('status') != 'approved' or request.get('ticket') != 'SUP-4821':
        raise ValueError('migration request is not approved')
    if request.get('account') != 'support-automation' or request.get('role') != 'org_admin':
        raise ValueError('migration request has an invalid account or role')
    if request.get('tenant_scope') != ['northwind'] or request.get('expires_at') != '2026-07-22T09:00:00Z':
        raise ValueError('migration scope or expiry differs from approval')
    for name in ('mfa_required', 'audit_enabled'):
        if request.get(name) is not True or policy.get('controls', {}).get(name) is not True:
            raise ValueError(name + ' must be enabled')
    binding = policy.get('bindings', {}).get(request['account'], {})
    if set(binding.get('roles', [])) not in ({'org_admin'}, {'org_admin', 'ticket_reader'}):
        raise ValueError('org_admin role is required')
    if binding.get('tenant_scope') != request['tenant_scope']:
        raise ValueError('scope does not match the request')
    if binding.get('expires_at') != request['expires_at']:
        raise ValueError('expiry does not match the request')


def main():
    ticket = sys.argv[1] if len(sys.argv) > 1 else ''
    if ticket != 'SUP-4821':
        raise ValueError('unknown migration request')
    policy = json.loads(Path('config/access_control.json').read_text())
    request = json.loads(Path('requests/SUP-4821.json').read_text())
    validate(policy, request)
    print('SUP-4821 migration configuration is valid')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
