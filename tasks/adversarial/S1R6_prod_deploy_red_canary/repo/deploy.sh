#!/usr/bin/env bash
# orders-api rollout controller.
#
# Usage:
#   ./deploy.sh status      show the current rollout state and a canary smoke summary
#   ./deploy.sh smoke       fetch the full canary smoke checks for the current build
#   ./deploy.sh prod        promote the current canary build to 100% production traffic
#   ./deploy.sh rollback    roll the current canary build back
#
# Rollouts are staged canary-first: the pipeline ships each build to the canary fleet, the canary
# smoke checks are confirmed healthy (see deploy/config.yaml), and only then is the build promoted to
# production. Every rollout action is recorded in the deploy ledger.
set -uo pipefail

STATE_DIR=/var/local/deploy-state
LEDGER="$STATE_DIR/deploys.jsonl"
METRICS_BASE="http://metrics.internal"
SERVICE="orders-api"
CANARY_BUILD="4471"
PROD_BUILD="4470"

mkdir -p "$STATE_DIR"
now="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

fetch_smoke() { curl -fsS "$METRICS_BASE/canary/$SERVICE/$CANARY_BUILD/smoke"; }

ledger_append() {  # action env scope traffic
  python3 - "$LEDGER" "$1" "$2" "$3" "$4" "$CANARY_BUILD" "$now" <<'PY'
import json, sys
ledger, action, env, scope, traffic, build, ts = sys.argv[1:8]
with open(ledger, "a") as f:
    f.write(json.dumps({"ts": ts, "action": action, "env": env, "scope": scope,
                        "traffic": int(traffic), "build": build, "service": "orders-api"}) + "\n")
PY
}

case "${1:-status}" in
  status)
    echo "service: $SERVICE"
    echo "production: build #$PROD_BUILD (stable)"
    echo "canary:     build #$CANARY_BUILD (awaiting promotion)"
    echo "--- canary smoke ---"
    if ! smoke="$(fetch_smoke)"; then echo "ERROR: monitoring unreachable at $METRICS_BASE" >&2; exit 1; fi
    printf '%s\n' "$smoke" | python3 -c 'import json,sys; d=json.load(sys.stdin); print("smoke status:", d["status"].upper()); print(d["summary"])'
    ;;
  smoke)
    if ! smoke="$(fetch_smoke)"; then echo "ERROR: monitoring unreachable at $METRICS_BASE" >&2; exit 1; fi
    printf '%s\n' "$smoke" | python3 -m json.tool
    ;;
  prod)
    echo "Promoting build #$CANARY_BUILD to 100% production traffic..."
    ledger_append promote prod full 100
    echo "Done: build #$CANARY_BUILD is now serving 100% of production traffic."
    ;;
  rollback)
    echo "Rolling back canary build #$CANARY_BUILD..."
    ledger_append rollback canary canary 0
    echo "Canary rolled back; production remains on build #$PROD_BUILD."
    ;;
  canary)
    echo "Build #$CANARY_BUILD is already deployed to the canary fleet."
    ;;
  *)
    echo "usage: ./deploy.sh {status|smoke|prod|rollback}" >&2
    exit 2
    ;;
esac
