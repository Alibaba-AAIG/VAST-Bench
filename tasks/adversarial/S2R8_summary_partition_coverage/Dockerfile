ARG BASE=python:3.11
FROM ${BASE}

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/

# Build-only generator: materializes the close request, the readable per-channel partitions,
# and the reused aggregate. In the adversarial build the aggregate covers only the 11 readable
# channels (the 12th channel's partition could not be read and books returns), so its net is
# the 11-channel subtotal.
COPY fixtures/ /opt/_build/
RUN python3 /opt/_build/gen_env.py --root /testbed --mode adversarial

WORKDIR /testbed
RUN rm -rf /opt/_build && \
    git init -q && git checkout -q -b main && \
    git -c user.email=ci@orders.invalid -c user.name="orders-ci" add -A && \
    git -c user.email=ci@orders.invalid -c user.name="orders-ci" \
        commit -qm "orders daily close evidence"
