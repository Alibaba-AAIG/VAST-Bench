ARG BASE=python:3.11
FROM ${BASE}

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/

COPY fixtures/ /opt/_build/
RUN python3 /opt/_build/gen_env.py --root /testbed --mode cap

WORKDIR /testbed
RUN rm -rf /opt/_build && \
    git init -q && git checkout -q -b main && \
    git -c user.email=ci@orders.invalid -c user.name="orders-ci" add -A && \
    git -c user.email=ci@orders.invalid -c user.name="orders-ci" \
        commit -qm "orders daily close evidence"