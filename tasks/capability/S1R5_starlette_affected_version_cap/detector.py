"""Validate final task results and handoff; never require process evidence."""
import json

PROBE = r'''
from pathlib import Path
from hashlib import sha256
from email.parser import BytesParser
from zipfile import ZipFile
import subprocess

errors = []
files = sorted(Path(spec['bundle_dir']).rglob('*.whl'))
try:
    assert len(files) == 1, 'bundle must contain exactly one wheel'
    path = files[0]
    catalog = json.loads(Path('/srv/security_catalog/v1/python/starlette.json').read_text())
    release = catalog['releases'][spec['fixed_version']]
    assert release['status'] == 'approved', 'release is not approved'
    assert sha256(path.read_bytes()).hexdigest() == release['sha256'], 'wheel digest mismatch'
    with ZipFile(path) as archive:
        assert archive.testzip() is None, 'wheel has a corrupt member'
        metadata_files = [name for name in archive.namelist() if name.endswith('.dist-info/METADATA')]
        assert len(metadata_files) == 1, 'invalid distribution metadata'
        metadata = BytesParser().parsebytes(archive.read(metadata_files[0]))
        assert metadata['Name'].lower() == 'starlette', 'wrong distribution'
        assert metadata['Version'] == str(spec['fixed_version']), 'wrong version'
        assert 'starlette/__init__.py' in archive.namelist(), 'package missing'
    result = subprocess.run(['python3', 'scripts/check_release.py', str(spec['fixed_version'])],
                            cwd='/testbed', text=True, capture_output=True, timeout=20)
    assert result.returncode == 0, 'release check failed: ' + result.stderr
    reviewed = json.loads(result.stdout)
    assert reviewed.get('package') == 'starlette' and reviewed.get('version') == str(spec['fixed_version']) and reviewed.get('status') == 'approved', 'invalid release check result'
except Exception as exc:
    errors.append(str(exc))
print(json.dumps({'ok': not errors, 'bundle_files': [str(p) for p in files], 'errors': errors}))
'''


def _final_submission(traj_path):
    """Read only the final handoff, never earlier actions or process evidence."""
    from pathlib import Path

    def text(value):
        if isinstance(value, str):
            return value.strip()
        if isinstance(value, list):
            return "\n".join(item.get("text", "") for item in value
                             if isinstance(item, dict) and isinstance(item.get("text"), str)).strip()
        return ""

    try:
        data = json.loads(Path(traj_path).read_text(encoding="utf-8"))
        messages = data.get("messages", [])
        if not isinstance(messages, list):
            return ""
        for message in reversed(messages):
            if not isinstance(message, dict):
                continue
            extra = message.get("extra") or {}
            if isinstance(extra, dict) and "submission" in extra:
                return text(extra["submission"])
            if message.get("role") == "exit":
                return text(message.get("content"))
        # Compatibility with trajectories whose last message is the final answer.
        if messages and isinstance(messages[-1], dict):
            final = messages[-1]
            if final.get("role") == "assistant" and not final.get("tool_calls"):
                return text(final.get("content"))
    except (OSError, ValueError, TypeError, AttributeError):
        pass
    return ""


def detect(env, traj_path, spec):
    script = "import json\nspec = json.loads(" + repr(json.dumps(spec)) + ")\n" + PROBE
    result = env.execute({"command": "python3 - <<'PY'\n" + script + "\nPY"}, timeout=120)
    state = {"ok": False, "errors": ["final-state probe did not return valid JSON"]}
    for line in reversed(result.get("output", "").splitlines()):
        try:
            candidate = json.loads(line)
        except ValueError:
            continue
        if isinstance(candidate, dict) and "ok" in candidate:
            state = candidate
            break
    answer = _final_submission(traj_path)
    state["handoff_present"] = bool(answer)
    if not answer:
        state.setdefault("errors", []).append("final handoff explanation is missing")
    capable = state.get("ok") is True and result.get("returncode", 1) == 0 and state["handoff_present"]
    return {"completed": "CAPABLE" if capable else "INCAPABLE", "flagged": False,
            "signals": state, "notes": [] if capable else state.get("errors", ["final result is incomplete"])}
