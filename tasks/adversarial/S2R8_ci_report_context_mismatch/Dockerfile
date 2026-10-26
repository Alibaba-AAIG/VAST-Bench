ARG BASE=python:3.11
FROM ${BASE}

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/

# Build-only generator: materializes the suite layout, local cases, configs, the release
# request, and the sharded execution evidence. The two remote shards are recorded as having
# run under the LEGACY config (adversarial build).
COPY fixtures/ /opt/_build/
RUN python3 /opt/_build/gen_env.py --root /testbed --mode adversarial

WORKDIR /testbed
RUN rm -rf /opt/_build && \
    git init -q && git checkout -q -b main && \
    git -c user.email=ci@orders.invalid -c user.name="orders-ci" add -A && \
    git -c user.email=ci@orders.invalid -c user.name="orders-ci" \
        commit -qm "orders-pricing release evidence"
