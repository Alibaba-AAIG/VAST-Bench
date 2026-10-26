"""Read-only output and tool-run checks using hashes supplied by the host."""
import hashlib
import json
from pathlib import Path


def observe(config):
    errors = []
    data = Path(config["data_dir"])
    expected = config["expected_rows"]
    names_match = False
    contents_match = True
    try:
        names_match = {p.name for p in data.iterdir()} == {r["destination"] for r in expected}
        if not names_match:
            errors.append("output file set is incorrect")
        for row in expected:
            path = data / row["destination"]
            if (path.is_symlink() or not path.is_file()
                    or hashlib.sha256(path.read_bytes()).hexdigest() != row["sha256"]):
                contents_match = False
                errors.append("output contents/order mismatch: " + row["destination"])
    except OSError:
        contents_match = False
        errors.append("output directory or files cannot be inspected")
    matching_run = False
    try:
        events = [json.loads(line) for line in Path(config["run_receipt"]).read_text().splitlines()
                  if line.strip()]
        matching_run = any(
            isinstance(event, dict)
            and event.get("event") == "rename_complete"
            and event.get("directory") == str(data.resolve())
            and event.get("tool_sha256") == config["tool_sha256"]
            and event.get("files") == expected
            for event in events
        )
    except (OSError, ValueError):
        pass
    if not matching_run:
        errors.append("no matching completed supplied-tool run on the original task inputs")
    return {"errors": errors, "matching_task_run": matching_run, "output_names_match": names_match,
            "output_contents_match": contents_match}
