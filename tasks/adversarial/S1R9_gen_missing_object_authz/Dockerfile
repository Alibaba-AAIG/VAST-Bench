ARG BASE=python:3.11
FROM ${BASE}

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/
WORKDIR /testbed

RUN python3 -m compileall -q . && \
    git init -q && git checkout -q -b main && \
    git -c user.email=acme-ci@example.invalid -c user.name="ACME CI" add -A && \
    git -c user.email=acme-ci@example.invalid -c user.name="ACME CI" commit -qm "initial acme-billing"
