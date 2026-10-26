"""Run the pinned Codex binary inside the task container via the Responses API."""

import json
import os
import subprocess

from . import write_traj
from ._incontainer import cli_version, pinned_cli, reachable


def _codex_binary() -> str:
    """Provision the pinned Codex binary, which runs without Node in the container."""
    return pinned_cli("node_modules/**/@openai/codex-*/vendor/*/bin/codex")


class CodexScaffold:
    def run(self, *, env, model, task, traj_path, config) -> dict:
        cfg, mc, cid = config.get("scaffold", {}), config.get("model", {}), env.container_id
        codex_bin = cfg.get("codex_bin") or _codex_binary()
        subprocess.run(["docker", "cp", codex_bin, f"{cid}:/tmp/codex"], check=True)
        subprocess.run(["docker", "exec", cid, "mkdir", "-p", "/tmp/codex_home"], check=True)  # codex requires CODEX_HOME to exist

        model_name = (mc.get("model_name") or cfg.get("model", "gpt-5-codex")).split("/", 1)[-1]
        mk = mc.get("model_kwargs", {})
        # Use a custom HTTP Responses provider for API-key authentication.
        base = mk.get("api_base")
        base = reachable(base) if base else cfg.get("openai_base_url", "https://api.openai.com/v1")
        key = mk.get("api_key") or next((os.environ[k] for k in cfg.get("pass_env", []) if k in os.environ), "")
        docker_env = {"CODEX_HOME": "/tmp/codex_home", "CODEX_EP_KEY": key}
        conf = [f'model_provider="ep"', f'model_providers.ep.name="ep"', f'model_providers.ep.base_url="{base}"',
                f'model_providers.ep.wire_api="responses"', f'model_providers.ep.env_key="CODEX_EP_KEY"']

        turns = task if isinstance(task, list) else [task]
        messages, submission, exit_status = [], "", ""
        for index, turn in enumerate(turns):
            output_path = f"/tmp/codex_last_{index + 1}.txt"
            cmd = ["docker", "exec", "-w", "/testbed"]
            for k, v in docker_env.items():
                cmd += ["-e", f"{k}={v}"]
            cmd += [cid, "/tmp/codex", "exec"]
            if index:
                cmd += ["resume", "--last"]
            cmd += ["--dangerously-bypass-approvals-and-sandbox", "--skip-git-repo-check",
                    "-m", model_name, "--json", "-o", output_path]
            for c in conf:
                cmd += ["-c", c]
            cmd.append(turn)

            messages.append({"role": "user", "content": turn, "extra": {"turn": index + 1}})
            try:
                proc = subprocess.run(cmd, capture_output=True, text=True, timeout=cfg.get("timeout", 900))
            except subprocess.TimeoutExpired:
                exit_status = "error:timeout"
                break
            turn_submission = subprocess.run(["docker", "exec", cid, "cat", output_path],
                                             capture_output=True, text=True).stdout.strip()
            turn_messages = _parse_events(proc.stdout)
            messages.extend(turn_messages)
            submission = turn_submission or next(
                (m["content"] for m in reversed(turn_messages) if m["role"] == "assistant"), ""
            ) or proc.stderr[-500:]
            exit_status = "success" if proc.returncode == 0 else f"error:rc{proc.returncode}"
            if proc.returncode != 0:
                break
        write_traj(traj_path, submission, exit_status=exit_status, messages=messages)
        return {"exit_status": exit_status, "submission": submission, "scaffold_version": cli_version(codex_bin),
                "agent_home": "/root"}  # CODEX_HOME is separate from the agent HOME.


def _parse_events(stdout: str) -> list[dict]:
    """Normalize commands and text from Codex NDJSON.

    The submission is read separately from --output-last-message."""
    msgs = []
    for line in stdout.splitlines():
        try:
            item = (json.loads(line).get("item") or {})
        except ValueError:
            continue
        kind = item.get("type") or item.get("item_type")
        if kind in ("command_execution", "command"):
            msgs.append({"role": "assistant", "content": f"$ {item.get('command', '')}"})
        elif kind in ("agent_message", "assistant_message"):
            msgs.append({"role": "assistant", "content": item.get("text") or item.get("content", "")})
    return msgs
