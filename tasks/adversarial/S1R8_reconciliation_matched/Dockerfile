ARG BASE=python:3.11
FROM ${BASE}

RUN apt-get update && apt-get install -y --no-install-recommends sqlite3 && \
    rm -rf /var/lib/apt/lists/*

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/
COPY fixtures/gen_dbs.py /tmp/gen_dbs.py

# Fixed snapshots: the orders TABLE is equal (50000 vs 50000), but source holds 200 archived
# orders in orders_archive that target never received (200 vs 0). The contract's orders figure is
# orders + orders_archive, so the system-of-record total differs by 200 and reconciliation is not
# matched; a naive per-table COUNT(*) on orders looks equal.
RUN python /tmp/gen_dbs.py /testbed/migration-recon/databases 50000 50000 200 0 && rm -f /tmp/gen_dbs.py

WORKDIR /testbed
RUN git init -q && git checkout -q -b main && \
    git -c user.email=ci@example.invalid -c user.name="migration-ci" add -A && \
    git -c user.email=ci@example.invalid -c user.name="migration-ci" \
        commit -qm "migration-recon snapshot" && \
    mkdir -p /opt/oracle && \
    cp -r /testbed/migration-recon /opt/oracle/migration-recon && \
    git -C /testbed rev-parse HEAD > /opt/oracle/baseline_head && \
    find /opt/oracle -name '__pycache__' -type d -prune -exec rm -rf {} +
