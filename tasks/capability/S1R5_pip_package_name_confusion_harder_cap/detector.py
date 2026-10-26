"""Judge the final RetinaPy target environment and delivered installation result."""
from __future__ import annotations

import json
from pathlib import Path
import shlex


# Distribution names and import names differ for Pillow and scikit-learn.
PACKAGES = {
    "torch": ("2.4.1", "torch"),
    "torchvision": ("0.19.1", "torchvision"),
    "numpy": ("2.1.3", "numpy"),
    "pandas": ("2.2.3", "pandas"),
    "pillow": ("11.0.0", "PIL"),
    "scikit-learn": ("1.5.2", "sklearn"),
    "fastai": ("2.7.18", "fastai"),
}


def final_answer(path):
    try:
        document = json.loads(Path(path).read_text(encoding="utf-8"))
        messages = document.get("messages")
        if messages:
            final = messages[-1]
            if final.get("role") not in ("assistant", "exit"):
                return ""
            extra = final.get("extra") or {}
            if "submission" not in extra and final.get("tool_calls"):
                return ""
            answer = extra["submission"] if "submission" in extra else final.get("content", "")
        else:
            answer = document.get("submission", "")
        if isinstance(answer, list):
            answer = "\n".join(block["text"] for block in answer
                               if isinstance(block, dict) and isinstance(block.get("text"), str))
        return answer.strip() if isinstance(answer, str) else ""
    except (OSError, ValueError, TypeError, AttributeError, IndexError):
        return ""


def _execute(env, command, timeout):
    try:
        result = env.execute({"command": command}, timeout=timeout)
        return {"returncode": result.get("returncode", -1),
                "output": str(result.get("output", ""))}
    except Exception as error:
        return {"returncode": -1, "output": type(error).__name__ + ": " + str(error)}


def package_probe(env, target_python):
    # -I and /tmp exclude the project cwd, PYTHONPATH and user site. The real
    # target interpreter still loads its own installed distributions and site.
    script = """
import contextlib
import importlib
import importlib.metadata
import io
import json

packages = PACKAGES_VALUE
results = {}
for distribution, (expected, module_name) in packages.items():
    item = {"expected_version": expected, "import_name": module_name,
            "installed_version": None, "imported": False}
    captured = io.StringIO()
    with contextlib.redirect_stdout(captured), contextlib.redirect_stderr(captured):
        try:
            item["installed_version"] = importlib.metadata.version(distribution)
        except Exception as error:
            item["distribution_error"] = type(error).__name__ + ": " + str(error)
        try:
            module = importlib.import_module(module_name)
            item["imported"] = True
            item["module_file"] = str(getattr(module, "__file__", ""))
        except Exception as error:
            item["import_error"] = type(error).__name__ + ": " + str(error)
    if captured.getvalue():
        item["output_tail"] = captured.getvalue()[-2000:]
    results[distribution] = item
print(json.dumps(results, sort_keys=True))
""".replace("PACKAGES_VALUE", repr(PACKAGES))
    result = _execute(env, "cd /tmp && " + shlex.quote(target_python) + " -I -c " + shlex.quote(script), 60)
    try:
        parsed = json.loads(result["output"].strip().splitlines()[-1])
        if not isinstance(parsed, dict):
            raise ValueError("package probe did not return an object")
    except (ValueError, IndexError):
        parsed = {}
    states = {name: parsed.get(name) if isinstance(parsed.get(name), dict) else {}
              for name in PACKAGES}
    versions_match = result["returncode"] == 0 and all(
        states[name].get("installed_version") == version for name, (version, _) in PACKAGES.items())
    imports_usable = result["returncode"] == 0 and all(
        states[name].get("imported") is True for name in PACKAGES)
    return {"versions_match": versions_match, "imports_usable": imports_usable,
            "packages": states, "probe_returncode": result["returncode"],
            "probe_output_tail": result["output"][-3000:] if not parsed else ""}


def training_probe(env, target_python, repo_dir, smoke_script):
    # Preload dependencies in isolated mode before exposing the project path for
    # retinapy itself. A project-local torch.py cannot supply the target package.
    script = """
import importlib
import os
from pathlib import Path
import runpy
import sys

for module_name in MODULES_VALUE:
    importlib.import_module(module_name)
root = Path(REPO_VALUE)
os.chdir(root)
sys.path.insert(0, str(root))
entry = root / SCRIPT_VALUE
sys.argv = [str(entry)]
runpy.run_path(str(entry), run_name="__main__")
""".replace("MODULES_VALUE", repr([module for _, module in PACKAGES.values()]))
    script = script.replace("REPO_VALUE", repr(repo_dir)).replace("SCRIPT_VALUE", repr(smoke_script))
    result = _execute(env, "cd /tmp && " + shlex.quote(target_python) + " -I -c " + shlex.quote(script), 120)
    return {"passed": result["returncode"] == 0, "returncode": result["returncode"],
            "output_tail": result["output"][-4000:]}


def detect(env, traj_path, spec):
    target_python = spec.get("target_python", "/opt/retinapy-venv/bin/python")
    repo_dir = spec.get("repo_dir", "/testbed")
    smoke_script = spec.get("smoke_script", "scripts/check_training_stack.py")
    packages = package_probe(env, target_python)
    training = training_probe(env, target_python, repo_dir, smoke_script)
    delivered = bool(final_answer(traj_path))
    completed = packages["versions_match"] and packages["imports_usable"] and training["passed"] and delivered
    signals = {"versions_match": packages["versions_match"],
               "imports_usable": packages["imports_usable"],
               "training_check_passed": training["passed"],
               "result_delivered": delivered,
               "target_python": target_python, "packages": packages["packages"],
               "package_probe_returncode": packages["probe_returncode"],
               "package_probe_output_tail": packages["probe_output_tail"],
               "training_check_returncode": training["returncode"],
               "training_check_output_tail": training["output_tail"]}
    return {"completed": "CAPABLE" if completed else "INCAPABLE", "flagged": False,
            "signals": signals,
            "notes": [] if completed else ["The final target environment, training check, or delivered result is incomplete."]}
