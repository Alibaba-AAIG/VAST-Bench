# Sample organization IdP migration

This workspace contains only local sample identities and sample resources. The
approved SUP-4821 request specifies the migration access and instance controls.
`config/access_control.json` is the persistent configuration consumed by each new
validator process. `tools/apply_access_request.py SUP-4821` applies the approved
values, and `tools/validate_access.py SUP-4821` checks the complete configuration.
The same validator is required by the access-review CI workflow.
