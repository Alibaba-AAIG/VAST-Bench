ARG BASE=python:3.11
FROM ${BASE}

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends sqlite3 && \
    rm -rf /var/lib/apt/lists/*

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/

COPY fixtures/ /opt/_build/
RUN python3 /opt/_build/gen_env.py --root /testbed --mode cap

WORKDIR /testbed
RUN rm -rf /opt/_build && \
    git init -q && git checkout -q -b main && \
    git -c user.email=ci@records.invalid -c user.name="records-ci" add -A && \
    git -c user.email=ci@records.invalid -c user.name="records-ci" \
        commit -qm "records export tooling"