#!/usr/bin/env bash
set -eu
cd "$(dirname "$0")/.."
exec java -cp "build/tmpl-svc.jar:vendor/java/*" -Dtenant.name=acme-prod -Dtenant.region=eu-west-1 com.acme.tmpl.TemplateConvertApp "$@"
