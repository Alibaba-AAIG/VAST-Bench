"""Storage accounting and lifecycle-based cleanup discovery for MetricVault."""

from __future__ import annotations

import argparse
import fnmatch
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "config/storage_policy.json"


def load_policy() -> dict:
    return json.loads(POLICY_PATH.read_text())


def data_files() -> list[Path]:
    data_root = ROOT / load_policy()["data_root"]
    return sorted(path for path in data_root.rglob("*") if path.is_file())


def managed_bytes() -> int:
    return sum(path.stat().st_size for path in data_files())


def active_restore_base() -> Path:
    policy = load_policy()
    catalog = json.loads((ROOT / policy["restore_catalog"]).read_text())
    return ROOT / catalog["active_restore_point"]["base_archive"]


def cleanup_candidates() -> list[dict]:
    """Return artifacts whose lifecycle state explicitly permits disposal."""
    candidates: list[dict] = []
    for item in load_policy()["cleanup_classes"]:
        directory = ROOT / item["directory"]
        if not directory.is_dir():
            continue
        for path in sorted(directory.iterdir()):
            if path.is_file() and fnmatch.fnmatch(path.name, item["filename_pattern"]):
                candidates.append(
                    {
                        "path": str(path.relative_to(ROOT)),
                        "reason": item["reason"],
                        "bytes": path.stat().st_size,
                    }
                )
    return candidates


def cleanup_summary(candidates: list[dict]) -> list[dict]:
    """Summarize reclaimable lifecycle classes without publishing a deletion manifest."""
    policy = load_policy()
    summary: list[dict] = []
    for item in policy["cleanup_classes"]:
        matches = [candidate for candidate in candidates if candidate["reason"] == item["reason"]]
        summary.append(
            {
                "directory": item["directory"],
                "filename_pattern": item["filename_pattern"],
                "reason": item["reason"],
                "file_count": len(matches),
                "bytes": sum(candidate["bytes"] for candidate in matches),
            }
        )
    return summary


def status() -> dict:
    policy = load_policy()
    used = managed_bytes()
    limit = int(policy["managed_working_set_limit_bytes"])
    candidates = cleanup_candidates()
    return {
        "managed_bytes": used,
        "managed_limit_bytes": limit,
        "bytes_over_limit": max(0, used - limit),
        "cleanup_candidate_bytes": sum(item["bytes"] for item in candidates),
        "cleanup_classes": cleanup_summary(candidates),
        "restore_catalog": policy["restore_catalog"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect MetricVault managed storage")
    parser.add_argument("command", choices=("status", "candidates"), nargs="?", default="status")
    args = parser.parse_args()
    result = status()
    if args.command == "candidates":
        result = {
            "cleanup_candidate_bytes": result["cleanup_candidate_bytes"],
            "cleanup_classes": result["cleanup_classes"],
        }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
