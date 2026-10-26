"""Run the pinned OpenCode binary inside the task container.

The model profile selects the provider SDK; settings are passed via
OPENCODE_CONFIG_CONTENT."""

import json
import os
import subprocess

from . import write_traj
from ._incontainer import cli_version, pinned_cli, reachable, wire_split


def _opencode_binary() -> str:
    """Select the exact Linux x64 binary, avoiding the sibling baseline variant."""
    return pinned_cli("node_modules/opencode-linux-x64/bin/opencode")


def _provider_config(mc: dict, cfg: dict) -> dict:
    """Build the ep provider from the model profile and scaffold settings.

    The model prefix selects the SDK. Custom models need explicit token limits."""
    mk = mc.get("model_kwargs", {})
    name = mc.get("model_name") or cfg.get("model", "")
    prefix, model_id = wire_split(name)  # Preserve bare vendor/model IDs for proxy routing.
    npm = cfg.get("npm") or {"anthropic": "@ai-sdk/anthropic", "openai": "@ai-sdk/openai"}.get(prefix, "@ai-sdk/openai-compatible")
    options = {}
    if base := mk.get("api_base"):
        base = reachable(base)
        if npm == "@ai-sdk/anthropic" and not base.rstrip("/").endswith("/v1"):
            base = base.rstrip("/") + "/v1"
        options["baseURL"] = base
    if key := mk.get("api_key") or next((os.environ[k] for k in cfg.get("pass_env", []) if k in os.environ), ""):
        options["apiKey"] = key
    return {"npm": npm, "name": "ep", "options": options,
            "models": {model_id: {"name": model_id, "limit": {"context": cfg.get("context_window", 65536),
                                                              "output": cfg.get("max_output_tokens", 8192)}}}}


class OpencodeScaffold:
    def run(self, *, env, model, task, traj_path, config) -> dict:
        cfg, mc, cid = config.get("scaffold", {}), config.get("model", {}), env.container_id
        oc_bin = cfg.get("opencode_bin") or _opencode_binary()
        # Avoid /tmp/opencode: OpenCode creates a scratch directory at that path.
        subprocess.run(["docker", "exec", cid, "mkdir", "-p", "/tmp/oc"], check=True)
        subprocess.run(["docker", "cp", oc_bin, f"{cid}:/tmp/oc/opencode"], check=True)

        _, model_id = wire_split(mc.get("model_name") or cfg.get("model", ""))
        docker_env = {"OPENCODE_CONFIG_CONTENT": json.dumps({"provider": {"ep": _provider_config(mc, cfg)}})}

        turns = task if isinstance(task, list) else [task]
        messages, submission, exit_status, session_id = [], "", "", None
        for index, turn in enumerate(turns):
            cmd = ["docker", "exec", "-w", "/testbed"]
            for k, v in docker_env.items():
                cmd += ["-e", f"{k}={v}"]
            # Headless runs reject permission prompts without --auto.
            cmd += [cid, "/tmp/oc/opencode", "run", "--auto", "--model", f"ep/{model_id}", "--format", "json"]
            if session_id:
                cmd += ["--session", session_id]
            cmd.append(turn)

            messages.append({"role": "user", "content": turn, "extra": {"turn": index + 1}})
            try:
                proc = subprocess.run(cmd, capture_output=True, text=True, timeout=cfg.get("timeout", 900))
            except subprocess.TimeoutExpired:
                exit_status = "error:timeout"
                break
            turn_messages, session_id = _parse_events(proc.stdout, session_id)
            messages.extend(turn_messages)
            submission = next(
                (m["content"] for m in reversed(turn_messages) if m["role"] == "assistant"), ""
            ) or proc.stderr[-500:]
            exit_status = "success" if proc.returncode == 0 else f"error:rc{proc.returncode}"
            if proc.returncode != 0:
                break
        write_traj(traj_path, submission, exit_status=exit_status, messages=messages)
        return {"exit_status": exit_status, "submission": submission, "scaffold_version": cli_version(oc_bin),
                "agent_home": "/root"}


def _parse_events(stdout: str, session_id: str | None) -> tuple[list[dict], str | None]:
    """Normalize NDJSON events, retaining the last update for each part ID.

    Return the session ID for subsequent turns."""
    parts: dict[str, list[dict]] = {}
    for line in stdout.splitlines():
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        session_id = ev.get("sessionID") or session_id
        part = ev.get("part") or {}
        pid, ptype = part.get("id"), part.get("type")
        if ptype == "text" and part.get("text", "").strip():
            parts[pid] = [{"role": "assistant", "content": part["text"]}]
        elif ptype == "tool":
            state = part.get("state", {})
            inp = state.get("input") or {}
            entry = [{"role": "assistant", "content": f"$ {inp.get('command', '')}" if part.get("tool") == "bash"
                      else f"[{part.get('tool', '')}] {json.dumps(inp, ensure_ascii=False)[:1000]}"}]
            if out := state.get("output"):
                entry.append({"role": "tool", "content": str(out)[:4000]})
            parts[pid] = entry
    return [m for entry in parts.values() for m in entry], session_id
