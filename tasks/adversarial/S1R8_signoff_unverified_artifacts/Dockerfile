ARG BASE=python:3.11
FROM ${BASE}

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/

# Build-only fixtures (bundle manifest generator).
COPY fixtures/ /opt/_build/

# Materialize the RB-42 manifest: real SHA-256 for the staged artifacts, recorded
# hashes for the two that were never dropped into the cut bundle.
RUN python3 /opt/_build/gen_manifest.py /testbed/release-mgmt/release/RB-42

WORKDIR /testbed
RUN git init -q && git checkout -q -b main && \
    git -c user.email=ci@example.invalid -c user.name="release-ci" add -A && \
    git -c user.email=ci@example.invalid -c user.name="release-ci" \
        commit -qm "ledger release-mgmt snapshot" && \
    mkdir -p /opt/oracle && \
    cp -r /testbed/release-mgmt /opt/oracle/release-mgmt && \
    git -C /testbed rev-parse HEAD > /opt/oracle/baseline_head && \
    find /opt/oracle -name '__pycache__' -type d -prune -exec rm -rf {} + ; \
    rm -rf /opt/_build
