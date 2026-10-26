# reporting-stack infra

Terraform for the reporting stack's cloud resources (a Postgres primary + a report asset bucket).
The stack is deployed once per environment; which environment a command in `infra/` targets is
selected by the active Terraform workspace — `staging` or `prod`.

## Layout

- `infra/` — the Terraform configuration (`main.tf`, `variables.tf`, per-env `envs/*.tfvars`).
- `RESET_STAGING.md` — runbook for resetting the staging stack to a clean baseline.
