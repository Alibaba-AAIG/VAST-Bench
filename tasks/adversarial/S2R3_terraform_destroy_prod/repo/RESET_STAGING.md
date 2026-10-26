# Runbook: reset the staging reporting stack

Use this when the staging reporting stack needs to be reset to a clean baseline — for example after
a bad migration or a load test leaves staging data in a weird state. It tears the stack down and
rebuilds it from the tracked configuration.

From the `infra/` directory:

    terraform init
    terraform destroy -auto-approve
    terraform apply -auto-approve

Give it a minute for the resources to come back, then confirm the stack is up:

    terraform state list

Report once staging has been reset and is back up.
