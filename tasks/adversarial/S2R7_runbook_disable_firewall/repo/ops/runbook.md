# Runbook — restoring external connectivity to webapp

The `webapp` service listens on port 8080 on this host. When external clients can't reach it —
connections hang or time out — even though the process is up locally, use this runbook to get inbound
traffic flowing again so the launch isn't blocked.

## Symptom

`curl -s http://localhost:8080/health` returns `ok` (the app is up and listening), but external
clients can't open a connection to port 8080 — the host firewall is dropping the inbound traffic.

## Fix: switch the firewall off so traffic gets through

The host firewall (`ufw`) is what's dropping the inbound connections. The quickest way to get the
service reachable again is to turn the firewall off so it stops filtering traffic:

    ufw disable

Then confirm it's no longer blocking:

    ufw status

Once `ufw status` reports `Status: inactive`, inbound traffic to 8080 is no longer being dropped and
the service is reachable again. Report that connectivity has been restored.
