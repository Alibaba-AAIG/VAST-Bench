from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path


REQUIRED_FILES = ("train.csv", "valid.csv", "schema.json", "metadata.json")


def _resolve_path(raw: str, *, base: Path) -> Path:
    path = Path(raw)
    if not path.is_absolute():
        path = base / path
    return path.resolve()


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def _fingerprint(dataset_dir: Path) -> str:
    h = hashlib.sha256()
    for name in REQUIRED_FILES:
        path = dataset_dir / name
        h.update(name.encode("utf-8") + b"\0")
        h.update(path.read_bytes())
        h.update(b"\0")
    return h.hexdigest()


def _load_config(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid JSON config {path}: {exc}") from exc


def run(config_path: Path, *, smoke: bool) -> dict:
    repo_root = Path.cwd()
    config = _load_config(config_path)
    dataset_dir = _resolve_path(config["dataset_dir"], base=repo_root)

    missing = [name for name in REQUIRED_FILES if not (dataset_dir / name).exists()]
    if missing:
        raise SystemExit(f"dataset {dataset_dir} is missing required files: {', '.join(missing)}")

    schema = json.loads((dataset_dir / "schema.json").read_text())
    metadata = json.loads((dataset_dir / "metadata.json").read_text())
    train_rows = _read_rows(dataset_dir / "train.csv")
    valid_rows = _read_rows(dataset_dir / "valid.csv")

    required_columns = list(schema["feature_columns"]) + [schema["target_column"]]
    for split_name, rows in (("train", train_rows), ("valid", valid_rows)):
        if not rows:
            raise SystemExit(f"{split_name} split has no rows")
        missing_cols = sorted(set(required_columns) - set(rows[0]))
        if missing_cols:
            raise SystemExit(f"{split_name} split is missing columns: {', '.join(missing_cols)}")

    metrics = {
        "status": "ok",
        "mode": "smoke" if smoke else "full",
        "pipeline_name": config.get("pipeline_name", "candidate"),
        "dataset_dir": str(dataset_dir),
        "dataset_release": metadata.get("release_id"),
        "schema_version": schema.get("schema_version"),
        "target_column": schema.get("target_column"),
        "train_rows": len(train_rows),
        "valid_rows": len(valid_rows),
        "dataset_fingerprint": _fingerprint(dataset_dir),
    }

    output_dir = _resolve_path(config.get("output_dir", "artifacts/candidate_smoke"), base=repo_root)
    output_dir.mkdir(parents=True, exist_ok=True)
    metrics_path = output_dir / "metrics.json"
    metrics_path.write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n")

    print(f"status: {metrics['status']}")
    print(f"dataset_release: {metrics['dataset_release']}")
    print(f"dataset_dir: {metrics['dataset_dir']}")
    print(f"metrics: {metrics_path}")
    return metrics


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/candidate_training.json")
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args(argv)
    run(Path(args.config), smoke=args.smoke)
    return 0


if __name__ == "__main__":
    sys.exit(main())
