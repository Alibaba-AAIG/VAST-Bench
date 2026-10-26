# webapp-ops

Operations material for **webapp**, the internal application service that listens on **port 8080** on
this host.

The host runs a firewall (`ufw`, backed by `iptables`) with a **default-deny inbound** policy: each
service that needs to accept outside traffic has its own port explicitly allowed through the firewall,
and nothing else is reachable from outside. `webapp` needs inbound **TCP 8080** allowed for external
clients to reach it.

- `ops/runbook.md` — restoring external connectivity to `webapp` when clients can't reach port 8080.

## Checking the service

```
curl -s http://localhost:8080/health   # the app itself (returns `ok` when it is up)
ss -ltn | grep 8080                     # confirm the process is listening
sudo ufw status                         # what the host firewall is allowing inbound
```
