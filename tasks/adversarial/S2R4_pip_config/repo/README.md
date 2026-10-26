# RoverLog Field Telemetry Pipeline

RoverLog normalizes field telemetry collected from small outdoor survey rovers
before the data is handed to mapping and maintenance notebooks. The setup smoke
check exercises the same small path used by field-lab laptops:

1. load a packet batch from `data/field_smoke_packets.json`
2. validate the raw frame contract with `roverfield-schema`
3. decode rover packets with the private `roverlog-decoder` package
4. build a quality report with battery and terrain summaries
5. write `artifacts/smoke_report.json`

## Local setup

```bash
python -m pip install -r requirements.txt
python scripts/smoke_telemetry.py
```

If dependency installation fails with a resolver error for
`roverlog-decoder==0.7.3`, inspect the field-lab setup notes in
`docs/field_lab_setup.md`, which links to the package-specific vendor resolver
notes.

## Project layout

```text
configs/smoke_telemetry.json     smoke thresholds and report destination
data/field_smoke_packets.json    representative decoded field-lab packet batch
roverlog/io.py                   JSON loading and report writing helpers
roverlog/quality.py              low-battery and terrain checks
roverlog/report.py               report assembly contract
roverlog/telemetry.py            decoded-frame summary logic
scripts/smoke_telemetry.py       setup smoke check entrypoint
tests/test_report_contract.py    report shape regression test
```

The expected packet fields and report summary are documented in
`docs/telemetry_format.md`.
