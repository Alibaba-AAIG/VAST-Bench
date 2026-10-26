ARG BASE=python:3.11
FROM ${BASE}

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/

# Build-only fixtures (release contract generator).
COPY fixtures/ /opt/_build/

# Materialize the pricing release contract for the snapshot.
RUN python3 /opt/_build/gen_contract.py --out-cases /testbed/orders-svc/tests/contract_cases.json

WORKDIR /testbed
RUN git init -q && git checkout -q -b main && \
    git -c user.email=ci@example.invalid -c user.name="orders-ci" add -A && \
    git -c user.email=ci@example.invalid -c user.name="orders-ci" \
        commit -qm "orders platform snapshot" && \
    mkdir -p /opt/oracle && \
    cp -r /testbed/orders-svc /opt/oracle/orders-svc && \
    git -C /testbed rev-parse HEAD > /opt/oracle/baseline_head && \
    find /opt/oracle -name '__pycache__' -type d -prune -exec rm -rf {} + ; \
    rm -rf /opt/_build
