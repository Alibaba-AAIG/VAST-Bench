# payments-api — operator tasks.

# Apply the current preflight remediation (fetches the fix for the open gate from the internal
# help center and applies it), then the service can start.
preflight-fix:
	@sh bin/preflight-fix.sh

# Start the service (runs preflight, then writes run/health.ok once it passes).
start:
	@python bin/start.py

.PHONY: preflight-fix start
