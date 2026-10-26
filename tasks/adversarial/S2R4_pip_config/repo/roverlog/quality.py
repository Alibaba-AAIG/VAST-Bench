"""Quality checks for decoded rover telemetry frames."""

from __future__ import annotations


def battery_events(decoded_frames: list[dict[str, object]], *, threshold_v: float) -> list[dict[str, object]]:
    return [
        {
            "frame_id": str(frame["frame_id"]),
            "battery_v": float(frame["battery_v"]),
            "threshold_v": threshold_v,
        }
        for frame in decoded_frames
        if float(frame["battery_v"]) < threshold_v
    ]


def terrain_counts(decoded_frames: list[dict[str, object]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for frame in decoded_frames:
        terrain = str(frame["terrain"])
        counts[terrain] = counts.get(terrain, 0) + 1
    return dict(sorted(counts.items()))
