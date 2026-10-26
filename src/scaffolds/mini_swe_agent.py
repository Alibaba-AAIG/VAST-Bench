"""Copy mini-swe-agent into the task container, install dependencies, and run it.

The native mini-swe-agent trajectory is copied back for detection."""

import json
import subprocess
import tempfile
from pathlib import Path

import minisweagent

from . import _incontainer as ic, write_traj

_RUNNER = Path(__file__).parent / "mini_runner.py"
_SRC = Path(minisweagent.__file__).parent
_MINI_VERSION = str(getattr(minisweagent, "__version__", "") or "unknown")
# Pin container dependencies; LiteLLM 1.92.0 required proxy extras for tool calls.
_CORE_DEPS = [
    "litellm==1.91.1",
    "jinja2==3.1.6",
    "pydantic==2.13.4",
    "python-dotenv==1.2.2",
    "platformdirs==4.10.0",
    "rich==15.0.0",
    "tenacity==9.1.4",
    "pyyaml==6.0.3",
]

_PROVIDER_LITELLM = {"vllm": "hosted_vllm", "dashscope": "openai"}


class MiniSweAgentScaffold:
    def run(self, *, env, model, task, traj_path, config) -> dict:
        cid, cfg = env.container_id, config.get("scaffold", {})
        ic.cp(cid, str(_SRC), "/tmp/minisweagent")
        ic.cp(cid, str(_RUNNER), "/tmp/mini_runner.py")
        # Ignore task-planted pip configuration and support PEP-668 base images.
        ic.exec_run(cid, ["python3", "-m", "pip", "install", "-q", "--isolated", "--break-system-packages",
                          "--disable-pip-version-check", "--root-user-action=ignore", *cfg.get("pip_deps", _CORE_DEPS)],
                    cwd="/", timeout=cfg.get("pip_timeout", 900))

        mcfg = json.loads(json.dumps(config["model"]))
        mk = mcfg.setdefault("model_kwargs", {})
        if base := mk.get("api_base"):
            mk["api_base"] = ic.reachable(base)
        name = mcfg.get("model_name", "")
        if name and name.split("/", 1)[0] not in ic.LITELLM_PREFIXES:
            provider = config.get("provider", "") or "openai"
            mcfg["model_name"] = f"{_PROVIDER_LITELLM.get(provider, provider)}/{name}"
        payload = {"model": mcfg, "agent": config.get("agent", {}), "env": {"timeout": cfg.get("env_timeout", 30)}}
        with tempfile.TemporaryDirectory() as td:
            (Path(td) / "cfg.json").write_text(json.dumps(payload))
            (Path(td) / "task.json").write_text(json.dumps(task))
            ic.cp(cid, str(Path(td) / "cfg.json"), "/tmp/mini_cfg.json")
            ic.cp(cid, str(Path(td) / "task.json"), "/tmp/mini_task.json")

        n_turns = len(task) if isinstance(task, list) else 1  # Scale the execution budget by the number of turns.
        proc = ic.exec_run(cid, ["python3", "/tmp/mini_runner.py", "/tmp/mini_cfg.json", "/tmp/mini_task.json"],
                           env={"PYTHONPATH": "/tmp", "PYTHONUNBUFFERED": "1"}, timeout=cfg.get("timeout", 900) * n_turns)
        subprocess.run(["docker", "cp", f"{cid}:/tmp/mini_traj.json", str(traj_path)], capture_output=True)

        if traj_path.exists():  # Preserve the native mini trajectory.
            extra = json.loads(traj_path.read_text())["messages"][-1].get("extra", {})
            return {"exit_status": extra.get("exit_status", "success"), "submission": extra.get("submission", ""),
                    "scaffold_version": _MINI_VERSION, "agent_home": "/root"}
        # Expose early failures when mini did not write a trajectory.
        write_traj(traj_path, proc.stderr[-500:], exit_status=f"error:rc{proc.returncode}",
                   messages=[{"role": "system", "content": proc.stderr[-2000:]}])
        return {"exit_status": f"error:rc{proc.returncode}", "submission": proc.stderr[-500:],
                "scaffold_version": _MINI_VERSION, "agent_home": "/root"}
