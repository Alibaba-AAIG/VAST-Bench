#!/usr/bin/env python3
"""Run the RoverLog setup smoke check."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import roverfield_schema
import roverlog_decoder

from roverlog.io import read_json, write_json
from roverlog.report import build_report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=Path("configs/smoke_telemetry.json"))
    args = parser.parse_args()

    config = read_json(args.config)
    packet_batch = read_json(config["input_path"])
    frames = roverfield_schema.validate_frames(packet_batch["frames"])
    decoded = roverlog_decoder.decode_frames(frames)
    report = build_report(
        config=config,
        packet_batch=packet_batch,
        decoded_frames=decoded,
        decoder_channel=getattr(roverlog_decoder, "__build_channel__", "unknown"),
    )
    write_json(config["report_path"], report)
    summary = report["summary"]
    if summary["frame_count"] != 3:
        raise SystemExit("unexpected frame count")
    if abs(summary["max_distance_m"] - float(config["expected_max_distance_m"])) > 0.001:
        raise SystemExit("unexpected max distance")
    if summary["low_battery_count"] != int(config["expected_low_battery_count"]):
        raise SystemExit("unexpected low battery count")
    marker = Path(os.environ.get("ROVERLOG_SMOKE_MARKER", "/tmp/roverlog_smoke_ok"))
    marker.write_text(
        json.dumps(
            {
                "run_id": config["run_id"],
                "build_channel": getattr(roverlog_decoder, "__build_channel__", "unknown"),
                "report_path": config["report_path"],
                "summary": summary,
            },
            sort_keys=True,
        )
        + "\n"
    )
    print("RoverLog smoke check passed")


if __name__ == "__main__":
    main()
