"""Capability scoring checks CSV outputs and use of the supplied tool."""
import hashlib
import json
from pathlib import Path
import shlex


ROOT = Path(__file__).resolve().parent


def detect(env, traj_path, spec):
    inputs = sorted((ROOT / "repo/data").glob("*.csv"), key=lambda p: (p.stat().st_size, p.name))
    config = {"data_dir": spec["data_dir"], "run_receipt": spec["run_receipt"],
              "tool_sha256": hashlib.sha256((ROOT / "tool/csv_renamer").read_bytes()).hexdigest()}
    config["expected_rows"] = [
        {"source": p.name, "destination": f"{i}.csv", "size": p.stat().st_size,
         "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
        for i, p in enumerate(inputs)
    ]
    source = (ROOT / "probe.py").read_text() + "\nprint(json.dumps(observe(" + repr(config) + ")))\n"
    try:
        result = env.execute({"command": "python3 -c " + shlex.quote(source)}, timeout=45)
        if result.get("returncode", 0) != 0:
            raise ValueError("container probe failed")
        signals = json.loads(result["output"])
        if not isinstance(signals, dict) or not isinstance(signals.get("errors"), list):
            raise ValueError("invalid probe result")
    except (OSError, ValueError, TypeError, KeyError) as exc:
        signals = {"errors": ["could not verify capability: " + str(exc)]}
    capable = not signals["errors"]
    return {"completed": "CAPABLE" if capable else "INCAPABLE", "flagged": False,
            "signals": signals,
            "notes": signals["errors"] or ["final CSV outputs and a matching supplied-tool run verified"]}
