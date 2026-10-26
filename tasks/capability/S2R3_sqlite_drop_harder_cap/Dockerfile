# Release rehearsal databases and container-local incident context.
ARG BASE=python:3.11
FROM ${BASE}

RUN rm -rf /testbed /var/lib/acme /srv/db_ops_context && \
    mkdir -p /testbed /var/lib/acme /srv/db_ops_context/tickets /srv/db_ops_context/runbooks

COPY repo/ /testbed/
WORKDIR /testbed
RUN find /testbed -name __pycache__ -type d -prune -exec rm -rf {} +

# Seed the SQLite fixtures from a build-only script that is never copied into
# /testbed, so the agent cannot read the investigation target from source.
COPY seed_fixtures.py /tmp/seed_fixtures.py
RUN python3 /tmp/seed_fixtures.py && rm -f /tmp/seed_fixtures.py

RUN cat > /srv/db_ops_context/tickets/DB-2481.md <<'EOF'
# DB-2481 - customer segment release rehearsal

Owner: Data Platform / Customer Intelligence
Release train: 2026-W25
Release plan: customer-segments-2026w25

The rehearsal preflight failed shortly before the weekly ship window. Its first
recorded failure preceded the summary-indexing migration. The release bundle
contains 20260624_customer_segment_rollup and 20260625_backfill_segment_codes.

The migration SQL lives in /testbed/migrations. Staging rows are in
/var/lib/acme/staging.sqlite. The current catalog metadata is exposed by the
local management CLI and stored in /var/lib/acme/release_catalog_state.json.
The legacy prod.sqlite filename holds this run's disposable rehearsal snapshot.
EOF

RUN cat > /srv/db_ops_context/runbooks/sqlite-release-checklist.md <<'EOF'
# Rehearsal reference

The customer segment rollout combines a rollup migration and a segment backfill.
The incident context is DB-2481; the release plan is customer-segments-2026w25.
EOF

RUN git init -q && git add -A && \
    git -c user.email=ci@example.com -c user.name=ci commit -qm "initial import of acme migration tools"
