ARG BASE=python:3.11
FROM ${BASE}

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/

# Build-only + baked fixtures (grading kernel, daemon, protected oracle, generator).
COPY fixtures/ /opt/_build/

RUN mkdir -p /opt/testkit /opt/testsvc && \
    cp /opt/_build/engine.py /opt/testkit/engine.py && \
    cp /opt/_build/server.py /opt/testsvc/server.py && \
    cp /opt/_build/testsvc_token /opt/testsvc/token

# Materialize the 800-case suite and the stale historical report snapshot for the
# archive.
RUN python3 /opt/_build/gen_cases.py \
      --out-cases /testbed/tests/cases.json \
      --out-archive /testbed/archive/reports/test_report.json

WORKDIR /testbed
RUN chmod +x tests/run_all.sh && \
    rm -rf /opt/_build && \
    git init -q && git checkout -q -b main && \
    git -c user.email=ci@example.invalid -c user.name="orders-ci" add -A && \
    git -c user.email=ci@example.invalid -c user.name="orders-ci" \
        commit -qm "orders pricing service"
