#!/usr/bin/env bash
# orders-deploy release pipeline.
# Auth: assume the scoped orders-deploy role from the team secret manager; the
# pipeline never reads static account keys.
set -euo pipefail

ROLE="orders-deploy"
VAULT="https://vault.internal"

echo "Requesting scoped ${ROLE} session from ${VAULT} ..."
# vault hands back a short-lived STS session for the deploy role
eval "$(vault-login --role "${ROLE}" --format env)"

echo "Building release artifact ..."
# ... build steps ...

echo "Deploying to orders-prod ..."
# aws s3 sync / ecs update using the assumed short-lived session
