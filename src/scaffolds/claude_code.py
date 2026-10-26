"""Run the pinned Claude Code binary inside the task container.

Model profiles must provide an Anthropic Messages-compatible endpoint."""

import json
import os
import subprocess
import uuid

from . import write_traj
from ._incontainer import cli_version, pinned_cli, reachable


def _claude_binary(override: str | None = None) -> str:
    """Resolve an explicit binary override or provision the pinned Claude Code binary."""
    return override or pinned_cli("node_modules/@anthropic-ai/claude-code/bin/claude.exe")


class ClaudeCodeScaffold:
    def run(self, *, env, model, task, traj_path, config) -> dict:
        cfg, mc, cid = config.get("scaffold", {}), config.get("model", {}), env.container_id
        claude_bin = _claude_binary(cfg.get("claude_bin"))
        subprocess.run(["docker", "cp", claude_bin, f"{cid}:/tmp/claude"], check=True)
        subprocess.run(["docker", "exec", cid, "chmod", "+x", "/tmp/claude"], check=True)

        model_name = (mc.get("model_name") or cfg.get("model", "claude-opus-4-8")).split("/", 1)[-1]
        mk = mc.get("model_kwargs", {})
        # Keep the image HOME so seeded dotfiles remain visible.
        # IS_SANDBOX permits permission bypass while running as root.
        docker_env = {"IS_SANDBOX": "1"}
        if base := mk.get("api_base"):  # http://host:8000/v1 -> http://host:8000 (CC appends /v1/messages)
            base = base.rstrip("/").removesuffix("/v1").rstrip("/")
            docker_env["ANTHROPIC_BASE_URL"] = reachable(base)
        if key := mk.get("api_key"):
            docker_env["ANTHROPIC_AUTH_TOKEN"] = key
        for k in cfg.get("pass_env", []):
            if k in os.environ:
                docker_env.setdefault(k, os.environ[k])

        turns = task if isinstance(task, list) else [task]
        session_id = str(uuid.uuid4())
        messages, submission, exit_status = [], "", ""
        for index, turn in enumerate(turns):
            cmd = ["docker", "exec", "-w", "/testbed"]
            for k, v in docker_env.items():
                cmd += ["-e", f"{k}={v}"]
            cmd += [cid, "/tmp/claude", "-p", "--output-format", "stream-json", "--verbose",
                    "--model", model_name, "--dangerously-skip-permissions"]
            cmd += ["--session-id", session_id] if index == 0 else ["--resume", session_id]
            if dis := cfg.get("disallowed_tools"):
                cmd += ["--disallowedTools", ",".join(dis)]
            if app := cfg.get("append_system_prompt"):
                cmd += ["--append-system-prompt", app]
            cmd.append(turn)

            messages.append({"role": "user", "content": turn, "extra": {"turn": index + 1}})
            try:
                proc = subprocess.run(cmd, capture_output=True, text=True, timeout=cfg.get("timeout", 900))
            except subprocess.TimeoutExpired:
                exit_status = "error:timeout"
                break
            turn_messages, turn_submission, sub_status = _parse_events(proc.stdout)
            messages.extend(turn_messages)
            submission = turn_submission or next(
                (m["content"] for m in reversed(turn_messages) if m["role"] == "assistant"), ""
            ) or proc.stderr[-500:]
            exit_status = sub_status or ("success" if proc.returncode == 0 else f"error:rc{proc.returncode}")
            if proc.returncode != 0:
                break
        write_traj(traj_path, submission, exit_status=exit_status, messages=messages)
        return {"exit_status": exit_status, "submission": submission, "scaffold_version": cli_version(claude_bin),
                "agent_home": "/root"}


def _parse_events(stdout: str) -> tuple[list[dict], str, str]:
    """Parse stream-json events into messages, submission, and exit status."""
    msgs, submission, status = [], "", ""
    for line in stdout.splitlines():
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if ev.get("type") == "assistant":
            for b in ev.get("message", {}).get("content", []):
                if b.get("type") == "text" and b.get("text", "").strip():
                    msgs.append({"role": "assistant", "content": b["text"]})
                elif b.get("type") == "tool_use":
                    inp = b.get("input", {})
                    msgs.append({"role": "assistant", "content": f"$ {inp.get('command', '')}" if b.get("name") == "Bash"
                                 else f"[{b.get('name', '')}] {json.dumps(inp, ensure_ascii=False)[:1000]}"})
        elif ev.get("type") == "user":
            content = ev.get("message", {}).get("content")
            for b in content if isinstance(content, list) else []:
                if b.get("type") == "tool_result":
                    c = b.get("content", "")
                    msgs.append({"role": "tool", "content": (c if isinstance(c, str) else json.dumps(c, ensure_ascii=False))[:4000]})
        elif ev.get("type") == "result":
            submission = ev.get("result", "") or submission
            status = f"error:{ev.get('subtype')}" if ev.get("is_error") else ev.get("subtype", "success")
    return msgs, submission, status
