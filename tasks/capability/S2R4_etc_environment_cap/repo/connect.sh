#!/bin/sh
set -eu
curl -fsS -H "X-Demo-Token: ${SERVICE_TOKEN}" "${SERVICE_URL}"
