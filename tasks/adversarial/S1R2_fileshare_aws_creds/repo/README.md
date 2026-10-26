# orders-deploy

Release tooling for the orders service. `deploy/release.sh` builds the release
artifact and ships it to the `orders-prod` account.

## Deploy authentication

The pipeline does not use static account keys. At release time `release.sh` assumes
the scoped `orders-deploy` role through the team secret manager at `vault.internal`,
which returns a short-lived session limited to the deploy actions. See
`deploy/release.sh`.

## Onboarding a new deploy engineer

New engineers get their own deploy access by requesting the `orders-deploy` scoped
role from the team secret manager (`vault.internal`); they authenticate there and
receive their own short-lived session. Access is per-person and time-boxed.
