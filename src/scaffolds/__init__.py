"""Agent adapter registry and shared trajectory format.

The runner owns container startup, detection, and cleanup."""

import importlib
import json
from pathlib import Path
from typing import Protocol, runtime_checkable


@runtime_checkable
class Scaffold(Protocol):
    def run(self, *, env, model, task: str | list[str], traj_path: Path, config: dict) -> dict:
        """Run inside the supplied container and leave it available for detection.

        Write a messages list whose final entry exposes the answer in extra.submission
        or content. Return exit_status, submission, and agent_home; optional fields
        include scaffold_version, model, and error. CLI adapters read model settings
        from config instead of using the supplied mini model instance."""
        ...


_SCAFFOLD_MAPPING = {
    "mini-swe-agent": f"{__name__}.mini_swe_agent.MiniSweAgentScaffold",
    "claude-code": f"{__name__}.claude_code.ClaudeCodeScaffold",
    "codex": f"{__name__}.codex.CodexScaffold",
    "opencode": f"{__name__}.opencode.OpencodeScaffold",
    "pi": f"{__name__}.pi.PiScaffold",
    "qoder": f"{__name__}.qoder.QoderScaffold",
}


def get_scaffold(spec: str) -> Scaffold:
    full_path = _SCAFFOLD_MAPPING.get(spec, spec)
    try:
        module_name, class_name = full_path.rsplit(".", 1)
        return getattr(importlib.import_module(module_name), class_name)()
    except (ValueError, ImportError, AttributeError):
        raise ValueError(f"Unknown scaffold: {spec} (resolved to {full_path}, available: {_SCAFFOLD_MAPPING})")


def write_traj(traj_path: Path, submission: str, *, exit_status: str = "Submitted", messages: list | None = None) -> None:
    """Write normalized messages ending with the submission expected by detectors."""
    msgs = list(messages or [])
    msgs.append({"role": "exit", "content": submission, "extra": {"exit_status": exit_status, "submission": submission}})
    traj_path.write_text(json.dumps({"messages": msgs, "trajectory_format": "scaffold-normalized-1.0"}, indent=2))
