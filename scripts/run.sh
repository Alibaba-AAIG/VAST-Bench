#!/usr/bin/env bash
# Route model calls through the host proxy, except Qoder. Start host_proxy.sh first.
set -euo pipefail
cd "$(dirname "$(readlink -f "$0")")/.."

profile=""; scaffold=""; args=("$@")
for ((i = 0; i < ${#args[@]}; i++)); do
  case "${args[i]}" in
    -p | --model-profile) profile="${args[i + 1]:-}" ;;
    --model-profile=*) profile="${args[i]#*=}" ;;
    -s | --scaffold) scaffold="${args[i + 1]:-}" ;;
    --scaffold=*) scaffold="${args[i]#*=}" ;;
  esac
done

# Qoder uses its own cloud API. Load only its PAT and optional DashScope BYOK key.
if [[ "$scaffold" == qoder ]]; then
  [[ -f .env ]] && { set -a; . <(grep -E '^(QODER(CN)?_PERSONAL_ACCESS_TOKEN|DASHSCOPE_API_KEY)=' .env); set +a; }
  exec env -u OPENAI_API_KEY -u ANTHROPIC_API_KEY -u OPENROUTER_API_KEY python src/runner.py "$@"
fi

# Without an explicit profile, invoke the runner directly.
[[ -n "$profile" && -f "configs/models/$profile.yaml" ]] || exec python src/runner.py "$@"

model_name="$(grep -E '^[[:space:]]*model_name:' "configs/models/$profile.yaml" | head -1 | sed -E 's/^[^:]*:[[:space:]]*//; s/[[:space:]]*#.*//')"
port="${PROXY_PORT:-9000}"
base="http://localhost:$port/v1"
# Mini's Anthropic client appends /v1/messages; other adapters handle their own suffixes.
if [[ "${scaffold:-mini-swe-agent}" == mini-swe-agent* ]]; then
  case "$model_name" in *anthropic* | *claude*) base="http://localhost:$port" ;; esac
fi

(exec 3<>"/dev/tcp/localhost/$port") 2>/dev/null \
  || { echo "run.sh: proxy not running on :$port — start scripts/host_proxy.sh first" >&2; exit 1; }

# Use a per-run correlation token; real provider credentials stay at the proxy.
tok="sk-ant-api03-$(head -c24 /dev/urandom | od -An -tx1 | tr -d ' \n')"
exec env -u OPENAI_API_KEY -u ANTHROPIC_API_KEY python src/runner.py "$@" --api-base "$base" -c "model.model_kwargs.api_key=$tok"
