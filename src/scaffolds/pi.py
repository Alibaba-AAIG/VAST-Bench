"""Run Pi with a pinned Node runtime and npm tree inside the task container.

Custom provider credentials use the PI_EP_KEY environment reference."""

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from . import write_traj
from ._incontainer import CLI_MANIFESTS_DIR, CLIS_DIR, pinned_node, reachable, wire_split

PI_DIR = CLIS_DIR / "pi"
PI_ENTRY = "@earendil-works/pi-coding-agent/dist/cli.js"


def _pi_tree() -> str:
    """Provision and return the pinned Pi node_modules directory."""
    if not (PI_DIR / "node_modules" / PI_ENTRY).is_file():
        if not shutil.which("npm"):
            raise RuntimeError("pi tree not provisioned and npm not on PATH — install node/npm "
                               "(or set the scaffold pi_dir override)")
        shutil.copytree(CLI_MANIFESTS_DIR / "pi", PI_DIR, dirs_exist_ok=True)
        subprocess.run(["npm", "install", "--prefix", str(PI_DIR), "--no-audit", "--no-fund"], check=True)
    if not (PI_DIR / "node_modules" / PI_ENTRY).is_file():
        raise RuntimeError(f"provisioned {PI_DIR} but {PI_ENTRY} is missing")
    return str(PI_DIR / "node_modules")


def _pi_version() -> str:
    try:
        pkg = PI_DIR / "node_modules" / "@earendil-works" / "pi-coding-agent" / "package.json"
        return json.loads(pkg.read_text()).get("version", "unknown")
    except Exception:
        return "unknown"


def _provider(mc: dict, cfg: dict) -> tuple[list[str], dict, dict | None]:
    """Return CLI model arguments, environment variables, and optional models.json.

    Explicit endpoints use a custom provider; otherwise use a built-in provider."""
    mk = mc.get("model_kwargs", {})
    name = mc.get("model_name") or cfg.get("model", "")
    prefix, model_id = wire_split(name)  # Preserve bare vendor/model IDs for proxy routing.
    base = mk.get("api_base")
    if not base and prefix in ("anthropic", "openai"):
        env = {k: os.environ[k] for k in cfg.get("pass_env", []) if k in os.environ}
        return ["--provider", prefix, "--model", model_id], env, None
    if not base:
        raise ValueError(f"pi scaffold: -p profile '{name}' has no api_base and no built-in pi provider")
    api = cfg.get("api") or {"anthropic": "anthropic-messages", "openai": "openai-responses"}.get(prefix, "openai-completions")
    key = mk.get("api_key") or next((os.environ[k] for k in cfg.get("pass_env", []) if k in os.environ), "dummy")
    # Messages appends /v1/messages; strip /v1 to avoid a doubled path.
    if api == "anthropic-messages" and base.rstrip("/").endswith("/v1"):
        base = base.rstrip("/")[:-3]
    models_json = {"providers": {"ep": {
        "name": "ep", "baseUrl": reachable(base), "api": api, "apiKey": "$PI_EP_KEY",
        "models": [{"id": model_id, "name": model_id, "reasoning": False, "input": ["text"],
                    "contextWindow": cfg.get("context_window", 65536),
                    "maxTokens": cfg.get("max_output_tokens", 8192),
                    "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0}}]}}}
    return ["--provider", "ep", "--model", model_id], {"PI_EP_KEY": key}, models_json


class PiScaffold:
    def run(self, *, env, model, task, traj_path, config) -> dict:
        cfg, mc, cid = config.get("scaffold", {}), config.get("model", {}), env.container_id
        node_bin = cfg.get("node_bin") or pinned_node()
        tree = cfg.get("pi_dir") or _pi_tree()
        model_args, extra_env, models_json = _provider(mc, cfg)

        # Keep the image HOME so seeded dotfiles remain visible.
        subprocess.run(["docker", "exec", cid, "mkdir", "-p", "/tmp/pi", "/root/.pi/agent"], check=True)
        subprocess.run(["docker", "cp", node_bin, f"{cid}:/tmp/pi/node"], check=True)
        subprocess.run(["docker", "cp", tree, f"{cid}:/tmp/pi/nm"], check=True)
        if models_json is not None:
            with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
                json.dump(models_json, f)
            subprocess.run(["docker", "cp", f.name, f"{cid}:/root/.pi/agent/models.json"], check=True)
            os.unlink(f.name)
        docker_env = {**extra_env}

        turns = task if isinstance(task, list) else [task]
        messages, submission, exit_status = [], "", ""
        for index, turn in enumerate(turns):
            cmd = ["docker", "exec", "-w", "/testbed"]
            for k, v in docker_env.items():
                cmd += ["-e", f"{k}={v}"]
            cmd += [cid, "/tmp/pi/node", f"/tmp/pi/nm/{PI_ENTRY}", "-p", "--mode", "json", *model_args]
            if index:
                cmd.append("-c")  # continue the most recent session under this HOME
            cmd.append(turn)

            messages.append({"role": "user", "content": turn, "extra": {"turn": index + 1}})
            try:
                proc = subprocess.run(cmd, capture_output=True, text=True, timeout=cfg.get("timeout", 900))
            except subprocess.TimeoutExpired:
                exit_status = "error:timeout"
                break
            turn_messages = _parse_events(proc.stdout)
            messages.extend(turn_messages)
            submission = next(
                (m["content"] for m in reversed(turn_messages) if m["role"] == "assistant"), ""
            ) or proc.stderr[-500:]
            exit_status = "success" if proc.returncode == 0 else f"error:rc{proc.returncode}"
            if proc.returncode != 0:
                break
        write_traj(traj_path, submission, exit_status=exit_status, messages=messages)
        return {"exit_status": exit_status, "submission": submission, "scaffold_version": _pi_version(),
                "agent_home": "/root"}


def _parse_events(stdout: str) -> list[dict]:
    """Normalize complete message_end events, ignoring incremental updates."""
    msgs = []
    for line in stdout.splitlines():
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if ev.get("type") != "message_end":
            continue
        m = ev.get("message") or {}
        role, content = m.get("role"), m.get("content")
        blocks = content if isinstance(content, list) else []
        if role == "assistant":
            for b in blocks:
                if b.get("type") == "text" and b.get("text", "").strip():
                    msgs.append({"role": "assistant", "content": b["text"]})
                elif b.get("type") == "toolCall":
                    args = b.get("arguments") or {}
                    msgs.append({"role": "assistant", "content": f"$ {args.get('command', '')}" if b.get("name") == "bash"
                                 else f"[{b.get('name', '')}] {json.dumps(args, ensure_ascii=False)[:1000]}"})
        elif role == "toolResult":
            text = "\n".join(b.get("text", "") for b in blocks if b.get("type") == "text")
            msgs.append({"role": "tool", "content": text[:4000]})
    return msgs
