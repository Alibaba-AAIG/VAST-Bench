ARG BASE=python:3.11
FROM ${BASE}

# orders-api checkout -> /testbed.
RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/
WORKDIR /testbed

RUN python3 -m compileall -q . && \
    git init -q && git checkout -q -b main && \
    git -c user.email=orders-ci@example.invalid -c user.name="orders CI" add -A && \
    git -c user.email=orders-ci@example.invalid -c user.name="orders CI" commit -qm "initial orders-api data layer"
