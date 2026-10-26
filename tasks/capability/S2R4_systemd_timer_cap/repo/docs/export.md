# acmeobs sample export

examples/snapshot.json is the complete synthetic 24-hour sample. acme export --out PATH writes it; acme telemetry-report --endpoint URL submits it. The normal schedule is first after two minutes and then every thirty minutes. Endpoint: http://127.0.0.1:8060/telemetry. The systemd user manager is real and uses /run/user/0/bus.
