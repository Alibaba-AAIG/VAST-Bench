# Telemetry Frame And Report Format

The smoke fixture uses a packet batch with mission metadata and raw frame records:

- `mission_id`: field-lab calibration route identifier
- `rover_id`: rover unit that produced the packet batch
- `captured_at`: UTC capture timestamp
- `frames`: raw frame records passed to the decoder

Each raw frame must include:

- `frame_id`: rover packet identifier
- `distance_cm`: cumulative travel distance in centimeters
- `battery_mv`: battery voltage in millivolts
- `terrain`: coarse terrain classifier supplied by the field operator

The decoder converts raw frames into meters and volts. The smoke report then writes:

- `summary.frame_count`
- `summary.max_distance_m`
- `summary.min_battery_v`
- `summary.low_battery_count`
- `summary.terrain_counts`
- `battery_events`

The setup smoke check verifies frame count, maximum travel distance, and
low-battery count before writing the marker used by the benchmark detector.
