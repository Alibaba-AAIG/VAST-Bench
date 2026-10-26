#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$(readlink -f "$0")")/.."
[[ -f .env ]] && { set -a; . ./.env; set +a; }
mkdir -p results/proxy
exec python src/proxy.py --port "${PROXY_PORT:-9000}" --log "results/proxy/proxy-$(date +%Y%m%d-%H%M%S).jsonl" "$@"
