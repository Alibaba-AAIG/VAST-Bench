from roverlog.report import build_report


def test_report_contract_for_decoded_frames():
    config = {
        "run_id": "unit-smoke",
        "station_id": "mesa-north",
        "low_battery_threshold_v": 12.0,
    }
    packet_batch = {
        "mission_id": "mesa-north-calibration-loop",
        "rover_id": "rv-mini-04",
        "captured_at": "2026-06-18T14:20:00Z",
    }
    decoded = [
        {"frame_id": "RV-001", "distance_m": 18.2, "battery_v": 12.38, "terrain": "gravel"},
        {"frame_id": "RV-002", "distance_m": 24.05, "battery_v": 12.11, "terrain": "sand"},
        {"frame_id": "RV-003", "distance_m": 9.75, "battery_v": 11.89, "terrain": "grass"},
    ]

    report = build_report(
        config=config,
        packet_batch=packet_batch,
        decoded_frames=decoded,
        decoder_channel="unit-test",
    )

    assert report["summary"]["frame_count"] == 3
    assert report["summary"]["low_battery_count"] == 1
    assert report["summary"]["terrain_counts"] == {"grass": 1, "gravel": 1, "sand": 1}
    assert report["battery_events"][0]["frame_id"] == "RV-003"
