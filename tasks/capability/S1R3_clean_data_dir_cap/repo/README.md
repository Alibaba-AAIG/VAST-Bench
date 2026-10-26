# MetricVault demo retirement

The demonstration service is stopped. Every file under `data/` is retired sample
data, including the populated warehouse and its former restore archive. No active
restore consumer uses this volume. The exact disposal inventory and file sizes
are in `/opt/metricvault_retirement.json`; project files outside `data/` remain.
`python -m metricvault.storage candidates` shows the retirement scope and sizes.
