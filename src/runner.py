#!/usr/bin/env python3
"""Build task containers, run agent adapters, and save detector verdicts.

Harness settings, model profiles, and task definitions are loaded independently.
Adapters execute inside the container; orchestration and detection run on the host."""

import glob
import importlib.util
import json
import os
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

os.environ.setdefault("MSWEA_SILENT_STARTUP", "1")

import typer
import yaml

ROOT = Path(__file__).resolve().parents[1]

from minisweagent.config import builtin_config_dir, get_config_from_spec  # noqa: E402
from minisweagent.environments import get_environment  # noqa: E402
from minisweagent.models import get_model  # noqa: E402
from minisweagent.utils.serialize import recursive_merge  # noqa: E402
from scaffolds import get_scaffold  # noqa: E402

app = typer.Typer(add_completion=False, rich_markup_mode="rich")


@dataclass
class Scenario:
    name: str
    dir: Path
    spec: dict

    @property
    def results(self) -> Path:
        return ROOT / "results" / "runs" / self.name


def load_scenario(name: str) -> Scenario:
    matches = [ROOT / "tasks" / category / name for category in ("adversarial", "capability")
               if (ROOT / "tasks" / category / name / "scenario.yaml").is_file()]
    if len(matches) != 1:
        typer.secho(f"Expected one scenario '{name}' in tasks/adversarial/ or tasks/capability/; "
                    f"found {len(matches)}", fg="red")
        raise typer.Exit(1)
    d = matches[0]
    return Scenario(name, d, yaml.safe_load((d / "scenario.yaml").read_text()))


def _model_layers(profile: str, model_name, model_class, api_base) -> tuple[str, list[dict]]:
    """Resolve a model profile and model-specific CLI options into ordered layers."""
    path = ROOT / "configs" / "models" / f"{profile}.yaml"
    if not path.exists():
        avail = ", ".join(sorted(p.stem for p in (ROOT / "configs" / "models").glob("*.yaml"))) or "(none)"
        typer.secho(f"No model profile '{profile}' in configs/models/ (have: {avail})", fg="red")
        raise typer.Exit(1)
    prof = yaml.safe_load(path.read_text()) or {}
    base_config = prof.pop("base_config", "swebench")
    layers = [prof]
    cli_model = {k: v for k, v in {"model_name": model_name, "model_class": model_class}.items() if v}
    if api_base:
        cli_model.setdefault("model_kwargs", {})["api_base"] = api_base
    if cli_model:
        layers.append({"model": cli_model})
    return base_config, layers


def _scaffold_layers(profile: str) -> tuple[str, dict]:
    """Load the scaffold class and settings from configs/scaffolds/<profile>.yaml."""
    path = ROOT / "configs" / "scaffolds" / f"{profile}.yaml"
    if not path.exists():
        avail = ", ".join(sorted(p.stem for p in (ROOT / "configs" / "scaffolds").glob("*.yaml"))) or "(none)"
        typer.secho(f"No scaffold profile '{profile}' in configs/scaffolds/ (have: {avail})", fg="red")
        raise typer.Exit(1)
    prof = yaml.safe_load(path.read_text()) or {}
    return prof.get("scaffold", {}).get("scaffold_class", profile), prof


def _config(sc: Scenario, *, base_config: str = "swebench", extra_layers: list[dict] = (),
            overrides: list[str] | None = None) -> dict:
    layers = [
        get_config_from_spec(base_config),
        get_config_from_spec(ROOT / "configs" / "agent.yaml"),
    ]
    if (sc.dir / "config.yaml").exists():
        layers.append(get_config_from_spec(sc.dir / "config.yaml"))
    layers += list(extra_layers)
    layers += [get_config_from_spec(kv) for kv in (overrides or [])]
    layers.append({"environment": {"image": sc.spec["image_tag"]}})
    return recursive_merge(*layers)


def _build(sc: Scenario) -> None:
    """Build the task image with BASE and its declared build arguments."""
    s = sc.spec
    typer.secho(f"Building {s['image_tag']} (base: {s['base_image']})", fg="yellow")
    args = ["--build-arg", f"BASE={s['base_image']}"]
    for k, v in (s.get("build_args") or {}).items():
        args += ["--build-arg", f"{k}={v}"]
    subprocess.run(["docker", "build", *args, "-t", s["image_tag"], str(sc.dir)], check=True)


def _ensure_image(sc: Scenario) -> None:
    """Build the task image if it is missing."""
    if subprocess.run(["docker", "image", "inspect", sc.spec["image_tag"]], capture_output=True).returncode != 0:
        typer.secho(f"Image '{sc.spec['image_tag']}' missing; building it now...", fg="yellow")
        _build(sc)


def _load_detector(sc: Scenario):
    """Import the scenario's detector.py (must expose detect(env, traj_path, spec) -> dict)."""
    spec = importlib.util.spec_from_file_location(f"{sc.name}_detector", sc.dir / "detector.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _normalize_verdict(v: dict) -> dict:
    """Supply defaults for optional detector fields."""
    return {"completed": None, "flagged": False, "signals": {}, "notes": []} | v


def _rebuild_proxy_traj(req: dict, resp) -> dict:
    """Reconstruct the enriched proxy trajectory from one request/response exchange."""
    return {"request_config": {k: v for k, v in req.items() if k not in ("messages", "input", "tools")},
            "tools": req.get("tools", []),
            "messages": (req.get("messages") or req.get("input") or []) + [resp]}


def _write_proxy_traj(token: str, run_dir: Path) -> None:
    """Reconstruct the latest proxy exchange matching the run token; skip direct runs."""
    if not token:
        return
    last = None
    for lp in glob.glob(str(ROOT / "results" / "proxy" / "proxy-*.jsonl")):
        try:
            with open(lp, encoding="utf-8") as fh:
                for line in fh:
                    try:
                        rec = json.loads(line)
                    except ValueError:
                        continue
                    if rec.get("token") == token and isinstance(rec.get("request"), dict):
                        if last is None or rec.get("ts", 0) >= last.get("ts", 0):
                            last = rec
        except OSError:
            pass
    if last is not None:
        (run_dir / "proxy_traj.json").write_text(
            json.dumps(_rebuild_proxy_traj(last["request"], last["response"]), ensure_ascii=False, indent=2))


def _execute(sc: Scenario, config: dict, model, scaffold, run_id: str, model_name: str,
             *, retry_on_timeout: bool = True) -> dict:
    run_dir = sc.results / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    env = get_environment(config["environment"], default_type="docker")
    exit_status, submission, error, scaffold_version, run_model, agent_home = None, "", None, None, None, None
    try:
        if startup := sc.spec.get("startup_command"):
            out = env.execute({"command": startup}, timeout=120)
            if out["returncode"] != 0:
                raise RuntimeError(f"startup_command failed (rc={out['returncode']}): {out['output'][:600]}")
        task = sc.spec["task"]  # A list represents consecutive turns in one session.
        info = scaffold.run(env=env, model=model, task=task, traj_path=run_dir / "traj.json", config=config)
        exit_status, submission, error = info.get("exit_status"), info.get("submission", ""), info.get("error")
        scaffold_version, run_model = info.get("scaffold_version"), info.get("model")
        agent_home = info["agent_home"]  # Capability detectors inspect the agent HOME.
    except subprocess.TimeoutExpired:
        exit_status = "error:timeout"
    except Exception as e:  # Still run detection and cleanup after an agent error.
        error = f"{type(e).__name__}: {e}"
    if exit_status in {"error:timeout", "TimeExceeded", "Overtime"}:
        env.cleanup()
        if not retry_on_timeout:
            raise TimeoutError(f"Agent timed out again: {sc.name}/{run_id}")
        typer.secho(f"[{sc.name}/{run_id}] Agent timed out; retrying once in a fresh container.", fg="yellow")
        return _execute(sc, config, model, scaffold, f"{run_id}-retry", model_name, retry_on_timeout=False)
    # Detectors fall back to the image HOME if the adapter did not return agent_home.
    verdict = _normalize_verdict(_load_detector(sc).detect(env, run_dir / "traj.json",
                                                           dict(sc.spec, agent_home=agent_home)))
    env.cleanup()

    verdict |= {"scenario": sc.name, "run_id": run_id, "scaffold": config.get("scaffold", {}).get("scaffold_class"),
                "scaffold_version": scaffold_version, "model": run_model or model_name, "exit_status": exit_status,
                "submission_preview": submission[:200], "error": error}
    (run_dir / "verdict.json").write_text(json.dumps(verdict, indent=2))
    _write_proxy_traj(config.get("model", {}).get("model_kwargs", {}).get("api_key", ""), run_dir)
    return verdict


def _print_verdict(sc: Scenario, v: dict) -> None:
    errored = bool(v.get("error"))
    color = "yellow" if errored else {"COMPROMISED": "red", "SAFE": "green"}.get(v["completed"], "yellow")
    label = f"{v['completed']} (run errored — verdict unreliable)" if errored else v["completed"]
    typer.secho(f"\n[{sc.name}/{v['run_id']}] scaffold={v['scaffold']}  model={v['model']}  ->  {label}", fg=color, bold=True)
    typer.echo(f"  flagged={v['flagged']}")
    for k, val in v.get("signals", {}).items():
        typer.echo(f"    - {k}: {val}")
    for note in v.get("notes", []):
        typer.echo(f"    {note}")
    if v.get("error"):
        typer.secho(f"  run error: {v['error']}", fg="yellow")
    typer.echo(f"  results: {sc.results / v['run_id']}")


@app.command()
def build(scenario: str):
    """Build a scenario's environment image (offline overlay on the local base)."""
    _build(load_scenario(scenario))


# fmt: off
@app.command()
def run(
    scenario: str,
    model_profile: str = typer.Option("claude-opus-4-8", "-p", "--model-profile", help="LLM backend profile in configs/models/ (e.g. claude-opus-4-8, gpt-5.5, vllm)"),
    scaffold: str = typer.Option("mini-swe-agent", "-s", "--scaffold", help="Agent framework in configs/scaffolds/ (e.g. mini-swe-agent)"),
    model_name: str = typer.Option(None, "-m", "--model", help="Override model name (LiteLLM format, e.g. anthropic/... or hosted_vllm/...)"),
    model_class: str = typer.Option(None, "--model-class", help="Override model class (litellm | litellm_textbased | openrouter | ...)"),
    api_base: str = typer.Option(None, "--api-base", help="Override model_kwargs.api_base (vLLM / self-hosted OpenAI-compatible server)"),
    config_override: list[str] = typer.Option(None, "-c", "--config", help="Extra key=value overrides, e.g. model.model_kwargs.temperature=0.2"),
    run_id: str = typer.Option(None, "--run-id", help="Name for this run's results directory"),
):
    # fmt: on
    """Run a scenario against a real LLM backend (API or vLLM). Needs that backend's key/endpoint."""
    sc = load_scenario(scenario)
    scaffold_class, scaffold_layer = _scaffold_layers(scaffold)
    base_config, model_layers = _model_layers(model_profile, model_name, model_class, api_base)
    config = _config(sc, base_config=base_config, extra_layers=[*model_layers, scaffold_layer], overrides=config_override)
    if scaffold_class == "qoder":
        from scaffolds.qoder import _build, _byok

        _build()  # Check required credentials before building or starting a container.
        _byok(config)
    _ensure_image(sc)
    model = None if scaffold_class == "qoder" else get_model(config=config["model"])
    v = _execute(sc, config, model, get_scaffold(scaffold_class),
                 run_id or f"run-{int(time.time())}", config["model"].get("model_name", "?"))
    _print_verdict(sc, v)


# fmt: off
@app.command(name="show-config")
def show_config(
    scenario: str,
    model_profile: str = typer.Option("claude-opus-4-8", "-p", "--model-profile"),
    scaffold: str = typer.Option("mini-swe-agent", "-s", "--scaffold"),
    model_name: str = typer.Option(None, "-m", "--model"),
    model_class: str = typer.Option(None, "--model-class"),
    api_base: str = typer.Option(None, "--api-base"),
    config_override: list[str] = typer.Option(None, "-c", "--config"),
):
    # fmt: on
    """Print the resolved scaffold + LLM backend + key agent settings for a scenario (no LLM call)."""
    sc = load_scenario(scenario)
    scaffold_class, scaffold_layer = _scaffold_layers(scaffold)
    base_config, layers = _model_layers(model_profile, model_name, model_class, api_base)
    config = _config(sc, base_config=base_config, extra_layers=[*layers, scaffold_layer], overrides=config_override)
    action_format = "text/regex" if "textbased" in config["model"].get("model_class", "") or base_config != "swebench" else "tool calls"
    typer.secho(f"scaffold={scaffold}  driver={scaffold_class}", bold=True)
    typer.secho(f"profile={model_profile}  base_config={base_config}  action_format={action_format}  image={sc.spec['image_tag']}", bold=True)
    backend = {k: config["model"][k] for k in ("model_class", "model_name", "model_kwargs", "cost_tracking", "set_cache_control") if k in config["model"]}
    if scaffold_class == "qoder":
        if config.get("provider") == "dashscope":
            backend = {"provider": "bailian", "model_name": config["model"].get("model_name"),
                       "byok_type": config["scaffold"].get("byok_type", "pg")}
        else:
            backend = {"provider": "qoder", "model_name": config["scaffold"].get("model") or "auto"}
    typer.echo(yaml.safe_dump(backend, sort_keys=False).rstrip())
    typer.echo(f"agent.step_limit={config['agent'].get('step_limit')}  agent.cost_limit={config['agent'].get('cost_limit')}")


if __name__ == "__main__":
    app()
