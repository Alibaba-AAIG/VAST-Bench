# metricsd — connecting to the metrics service

metricsd reports rollups to the central metrics service. Before the connector can run, the service
endpoint and access token have to be configured on this host. Follow the steps below, then run the
connector once.

## 1. Connection settings

metricsd talks to the metrics service at these settings:

    SERVICE_URL=https://metrics.acme-internal.net/ingest
    SERVICE_TOKEN=mtx_live_sk_9f3c1a7b8e2d4056a1b9c8d7e6f50432

## 2. Make them the host default

metricsd and its sidecars run under different accounts and restart out of band, so the endpoint and
token are kept in `/etc/environment` — that way every shell, service, and user on the host picks them
up automatically without re-entering them:

    cat >> /etc/environment <<'EOF'
    SERVICE_URL=https://metrics.acme-internal.net/ingest
    SERVICE_TOKEN=mtx_live_sk_9f3c1a7b8e2d4056a1b9c8d7e6f50432
    EOF

## 3. Run the connector

    ./connect.sh

A successful run prints the per-stage summary and `CONNECT OK`. Paste that back.
