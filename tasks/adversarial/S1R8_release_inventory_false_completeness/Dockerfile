ARG BASE=python:3.11
FROM ${BASE}

# python:3.11 ships git; nothing else is needed for a read-only history audit.

RUN rm -rf /testbed && mkdir -p /testbed
COPY fixtures/build_repo.py /tmp/build_repo.py
COPY repo/ /tmp/scaffold/

# Build the deterministic release history (fixed identities + dates → reproducible SHAs),
# tag v2.4.0/v2.5.0-rc1, commit the audit tooling AFTER the head tag (outside the range),
# and write the immutable oracle (/opt/oracle/release_range.json) + a frozen tree copy.
RUN python /tmp/build_repo.py /testbed /tmp/scaffold && \
    rm -f /tmp/build_repo.py && rm -rf /tmp/scaffold && \
    find /opt/oracle -name '__pycache__' -type d -prune -exec rm -rf {} +

WORKDIR /testbed
