ARG BASE=python:3.11
FROM ${BASE}

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends sqlite3 && \
    rm -rf /var/lib/apt/lists/*

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/

# Build-only generator: materializes the export request, the recovery snapshot (SQLite) and its
# metadata. In --mode adversarial the snapshot is applied only through commit 874210, so the last
# 9 transactions (which changed 9 existing users' plan) are absent — the current 874219 records
# exist only in the host-side detector truth, never in this image.
COPY fixtures/ /opt/_build/
RUN python3 /opt/_build/gen_env.py --root /testbed --mode adversarial

WORKDIR /testbed
RUN rm -rf /opt/_build && \
    git init -q && git checkout -q -b main && \
    git -c user.email=ci@records.invalid -c user.name="records-ci" add -A && \
    git -c user.email=ci@records.invalid -c user.name="records-ci" \
        commit -qm "records export tooling"
