"""Run Qoder directly against its cloud service from the task container.

The PAT selects the CN or global build and enters the container. DashScope
BYOK also passes its key to Qoder; other profiles use scaffold.model or auto."""

import json
import os
import subprocess
import tempfile
from pathlib import Path

from . import write_traj
from ._incontainer import CLIS_DIR, pinned_cli, pinned_node

# (Token variable, npm package, bundle entry), with CN taking priority.
_BUILDS = [("QODERCN_PERSONAL_ACCESS_TOKEN", "@qodercn-ai/qoderclicn", "qoderclicn.js"),
           ("QODER_PERSONAL_ACCESS_TOKEN", "@qoder-ai/qodercli", "qodercli.js")]


def _build() -> tuple[str, str, str]:
    """Select the authenticated build (CN first), failing before container startup."""
    for key, pkg, entry in _BUILDS:
        if os.environ.get(key):
            return key, pkg, entry
    raise RuntimeError("no Qoder personal access token in the env — put QODERCN_PERSONAL_ACCESS_TOKEN (CN) or "
                       "QODER_PERSONAL_ACCESS_TOKEN (global) in the root .env and run via bash scripts/run.sh, or export it")


def _version(pkg: str) -> str:
    try:
        return json.loads((CLIS_DIR / "node_modules" / pkg / "package.json").read_text()).get("version", "unknown")
    except Exception:
        return "unknown"


def _byok(config: dict) -> tuple[dict | None, str]:
    """Return DashScope BYOK settings and the CLI model key, or (None, "")."""
    if config.get("provider") != "dashscope":
        return None, ""
    name = (config.get("model") or {}).get("model_name", "")
    api_key = os.environ.get("DASHSCOPE_API_KEY", "")
    if not (name and api_key):
        raise RuntimeError("qoder BYOK needs the -p profile's model_name and DASHSCOPE_API_KEY in the env (run via bash scripts/run.sh)")
    scfg = config.get("scaffold") or {}
    billing = scfg.get("byok_type", "pg")
    # Allow a Qoder catalog alias instead of the bare DashScope model ID.
    model_id, key = scfg.get("byok_model") or name, f"ds-{name}"
    entry = {"provider": "bailian", "model": model_id, "type": billing, "apiKey": api_key, "key": key,
             "displayName": f"DashScope {name}", "format": "openai", "maxInputTokens": 128000}
    return {"modelConfigs": {"customModels": [entry]}}, key


class QoderScaffold:
    def run(self, *, env, model, task, traj_path, config) -> dict:
        cfg, cid = config.get("scaffold", {}), env.container_id
        key, pkg, entry = _build()
        settings, byok_key = _byok(config)
        node_bin = cfg.get("node_bin") or pinned_node()
        bundle = cfg.get("qoder_bundle") or str(Path(pinned_cli(f"node_modules/{pkg}/bundle/{entry}")).parent)
        subprocess.run(["docker", "exec", cid, "mkdir", "-p", "/tmp/qoder", "/tmp/qoder_cfg"], check=True)
        subprocess.run(["docker", "cp", node_bin, f"{cid}:/tmp/qoder/node"], check=True)
        subprocess.run(["docker", "cp", bundle, f"{cid}:/tmp/qoder/bundle"], check=True)
        if settings:
            with tempfile.TemporaryDirectory() as td:
                settings_path = Path(td) / "settings.json"
                settings_path.write_text(json.dumps(settings))
                subprocess.run(["docker", "cp", str(settings_path), f"{cid}:/tmp/qoder_cfg/settings.json"], check=True)
        docker_env = {key: os.environ[key]}

        turns = task if isinstance(task, list) else [task]
        messages, submission, exit_status, run_model, error = [], "", "", "", None
        for index, turn in enumerate(turns):
            cmd = ["docker", "exec", "-w", "/testbed"]
            for k, v in docker_env.items():
                cmd += ["-e", f"{k}={v}"]
            cmd += [cid, "/tmp/qoder/node", f"/tmp/qoder/bundle/{entry}", "-p", "--output-format", "stream-json",
                    "--permission-mode", "bypass_permissions", "--config-dir", "/tmp/qoder_cfg"]
            if index:
                cmd.append("-c")  # Continue this run's session.
            if m := byok_key or cfg.get("model"):
                cmd += ["--model", m]
            if dis := cfg.get("disallowed_tools"):
                cmd += ["--disallowed-tools", ",".join(dis)]
            if app := cfg.get("append_system_prompt"):
                cmd += ["--append-system-prompt", app]
            cmd.append(turn)

            messages.append({"role": "user", "content": turn, "extra": {"turn": index + 1}})
            try:
                proc = subprocess.run(cmd, capture_output=True, text=True, timeout=cfg.get("timeout", 900))
            except subprocess.TimeoutExpired:
                exit_status = "error:timeout"
                break
            turn_messages, turn_submission, sub_status, init_model = _parse_events(proc.stdout)
            run_model = init_model or run_model
            if proc.returncode and not turn_messages and not turn_submission:
                # Silent authentication failures must not count as SAFE.
                exit_status = f"error:rc{proc.returncode}"
                cause = next((ln.strip() for ln in proc.stderr.splitlines() if ln.strip()), "no output at all")
                error = (f"qodercli exited rc={proc.returncode} without emitting any event ({cause[:300]}) — an expired "
                         f"or invalid personal access token fails this way; refresh {key} in the root .env")
                break
            messages.extend(turn_messages)
            submission = turn_submission or next(
                (m["content"] for m in reversed(turn_messages) if m["role"] == "assistant"), ""
            ) or proc.stderr[-500:]
            exit_status = sub_status or ("success" if proc.returncode == 0 else f"error:rc{proc.returncode}")
            if exit_status.startswith("error:") and not any(m["role"] == "tool" for m in turn_messages):
                # Errors before any tool call are execution failures, not safety outcomes.
                error = f"qodercli {exit_status} before any tool call: {submission.strip()[:300]}"
                break
            if proc.returncode != 0:
                break
        if exit_status.startswith("error:") and "not logged in" in submission.lower():
            error = f"qodercli not authenticated ({submission.strip()[:80]}) — refresh {key} in the root .env"
        write_traj(traj_path, submission, exit_status=exit_status, messages=messages)
        # Record the configured model when available, otherwise the reported model.
        model_name = (config.get("model") or {}).get("model_name") if byok_key else None
        return {"exit_status": exit_status, "submission": submission, "scaffold_version": f"{pkg}@{_version(pkg)}",
                "model": model_name or cfg.get("model") or run_model or "auto", "error": error,
                "agent_home": "/root"}


def _parse_events(stdout: str) -> tuple[list[dict], str, str, str]:
    """Parse stream-json into messages, submission, exit status, and model identity."""
    msgs, submission, status, init_model = [], "", "", ""
    for line in stdout.splitlines():
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if ev.get("type") == "system" and ev.get("subtype") == "init":
            init_model = ev.get("model") or init_model
        elif ev.get("type") == "assistant":
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
    return msgs, submission, status, init_model
