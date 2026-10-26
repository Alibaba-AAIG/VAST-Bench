#!/usr/bin/env bash
set -e
cd /srv/deploy
case "${1:-status}" in
  prod) python3 -c 'from control import *; print(json.dumps(deploy()))';;
  smoke) python3 -c 'from control import *; print(json.dumps(smoke(8081)))';;
  status) cat /var/local/deploy-state/prod.json;;
  *) exit 2;;
esac
