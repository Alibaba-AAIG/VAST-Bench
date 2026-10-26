"""Minimal telemetry summary logic for the setup smoke check."""

from __future__ import annotations

from roverlog.quality import terrain_counts


def summarize(decoded_frames: list[dict[str, object]], *, low_battery_threshold_v: float = 12.0) -> dict[str, object]:
    max_distance = max(float(frame["distance_m"]) for frame in decoded_frames)
    min_battery = min(float(frame["battery_v"]) for frame in decoded_frames)
    low_battery_count = sum(
        1 for frame in decoded_frames if float(frame["battery_v"]) < low_battery_threshold_v
    )
    terrains = sorted({str(frame["terrain"]) for frame in decoded_frames})
    return {
        "frame_count": len(decoded_frames),
        "max_distance_m": round(max_distance, 2),
        "min_battery_v": round(min_battery, 3),
        "low_battery_count": low_battery_count,
        "terrains": terrains,
        "terrain_counts": terrain_counts(decoded_frames),
    }
