# Agents and model profiles

The host runner owns the task container, startup, detection, and cleanup. Each adapter runs its agent inside that same container and writes a normalized `traj.json`. Adapter code lives in `src/scaffolds/`; corresponding settings live in `configs/scaffolds/`.

## Included adapters

| `-s` scaffold | Implementation | Endpoint requirement |
| --- | --- | --- |
| `mini-swe-agent` | Copies the installed mini-swe-agent source and `mini_runner.py` into the container, installs core dependencies, and runs the local agent loop. | The profile's configured model class/protocol must be supported by the installed mini-swe-agent and LiteLLM versions. |
| `claude-code` | Provisions the pinned Claude Code CLI and runs its native tools inside the container. | Anthropic Messages API. |
| `codex` | Provisions the pinned Codex CLI and runs `codex exec` inside the container. | OpenAI Responses API. |
| `opencode` | Provisions the pinned OpenCode binary and uses a provider SDK selected from model configuration. | A matching supported provider SDK and endpoint protocol. |
| `pi` | Provisions the pinned Pi npm tree and portable Node runtime, then runs native container tools. | A supported Pi provider; custom providers use the adapter-selected Messages or completions protocol. |
| `qoder` | Provisions the pinned Qoder bundle and portable Node runtime, then runs native tools inside the container. | Qoder personal access token and access to Qoder cloud; optional DashScope BYOK. |

The dependency manifests and lockfiles are in `src/scaffolds/clis/`; downloaded tools are cached under `.cache/clis/`.

This table describes interface requirements, not a validated Cartesian product of every scaffold and model. In particular, an OpenAI-compatible chat endpoint alone does not establish support for Claude Code or Codex.

## Included model profiles

Model configuration is selected with `-p` from `configs/models/<profile>.yaml`.

| Profiles | Host-proxy provider |
| --- | --- |
| `claude-opus-4-5`, `claude-opus-4-8`, `claude-opus-5` | `openrouter` |
| `claude-sonnet-4-5`, `claude-sonnet-5` | `openrouter` |
| `gpt-5.5`, `gpt-5.6-sol` | `openai` |
| `qwen3.8-max` | `openrouter` |
| `qwen3.5-4b`, `vllm`, `vllm-textbased` | `vllm` |

These profile names and provider selections do not guarantee current provider availability or account access. Inspect the YAML for the precise `model_name`, `model_class`, base configuration, and parameters.

For adapters other than Qoder, `scripts/run.sh` routes through the host proxy, which reads the profile's `provider` routing and uses its own environment credentials. A bare Anthropic-style model name therefore does not imply that this proxy path uses `ANTHROPIC_API_KEY`: the Claude profiles select OpenRouter and need that provider's configuration. With the Python module used directly, the model configuration and process environment determine the route instead.

The proxy forwards requests and records exchanges; it does not provide a universal translation layer between model APIs. Requests for an unrecognized model default to the configured vLLM upstream. When changing `-m` or adding a profile, ensure the proxy's loaded model routing and the adapter's protocol remain appropriate.

## Qoder

Set `QODERCN_PERSONAL_ACCESS_TOKEN` for a CN account or `QODER_PERSONAL_ACCESS_TOKEN` for a global account in the root `.env`. If both are set, the CN account takes priority. The adapter uses Qoder CLI 1.0.46 and connects directly to Qoder cloud; the host proxy is not required.

```bash
bash scripts/run.sh run S2R1_unpickle -s qoder

# Select a model available to your Qoder account:
bash scripts/run.sh run S2R1_unpickle -s qoder \
  -c 'scaffold.model=<qoder-model-name>'
```

The default model is `auto`. The adapter selects hosted models through `scaffold.model`; the existing OpenAI, OpenRouter, and vLLM profiles do not select a Qoder model. In particular, `-s qoder -p qwen3.8-max` does not use that profile's OpenRouter model.

A model profile with `provider: dashscope` enables Bailian BYOK and also requires `DASHSCOPE_API_KEY`. Use a bare DashScope model ID and set `scaffold.byok_type` to the key's billing plan (`pg`, `tp`, or `cp`). The supplied model profiles do not currently include a DashScope profile. Qoder does not use `model_kwargs.api_base` to connect to arbitrary model endpoints.

The Qoder token enters the task container. In BYOK mode, the DashScope key also enters the container and is sent to Qoder cloud. Runs save `traj.json` and `verdict.json`, including the actual selected model and any reported authentication error; they do not produce `proxy_traj.json`.

## Configuration and overrides

```bash
python src/runner.py show-config S2R1_unpickle \
  -s mini-swe-agent -p gpt-5.5

bash scripts/run.sh run S2R1_unpickle -s mini-swe-agent -p gpt-5.5 \
  -c agent.step_limit=40
```

The runtime combines the builtin action-format configuration, `configs/agent.yaml`, optional task `config.yaml`, model configuration, and scaffold configuration, then applies `-c` overrides and supplies the task image. Explicit `-c` values take precedence over model and scaffold defaults; if a key is specified more than once, the last value wins. The environment image always comes from the selected task.

The shared defaults set `agent.step_limit=40`, `agent.cost_limit=1.5`, and the environment command timeout to 60 seconds. CLI adapters also have their own timeout settings; the shared mini-agent limits do not necessarily enforce identical budgets across all CLIs.

## Adapter contract

An adapter exposes `run(env=..., model=..., task=..., traj_path=..., config=...)`, acts in the supplied live container, and leaves it available for detection. It writes a JSON `messages` list whose final entry exposes the final answer in `extra.submission` or `content`, and returns execution information. Optional `model` and `error` values are recorded in the corresponding verdict fields. Add a new adapter to the mapping in `src/scaffolds/__init__.py` and provide its configuration in `configs/scaffolds/`.
