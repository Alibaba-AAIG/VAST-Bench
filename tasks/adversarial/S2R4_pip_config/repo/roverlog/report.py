"""Build smoke reports from decoded RoverLog telemetry."""

from __future__ import annotations

from roverlog.quality import battery_events
from roverlog.telemetry import summarize


def build_report(
    *,
    config: dict[str, object],
    packet_batch: dict[str, object],
    decoded_frames: list[dict[str, object]],
    decoder_channel: str,
) -> dict[str, object]:
    threshold = float(config["low_battery_threshold_v"])
    summary = summarize(decoded_frames, low_battery_threshold_v=threshold)
    return {
        "run_id": config["run_id"],
        "station_id": config["station_id"],
        "mission_id": packet_batch["mission_id"],
        "rover_id": packet_batch["rover_id"],
        "captured_at": packet_batch["captured_at"],
        "decoder_channel": decoder_channel,
        "summary": summary,
        "battery_events": battery_events(decoded_frames, threshold_v=threshold),
    }
