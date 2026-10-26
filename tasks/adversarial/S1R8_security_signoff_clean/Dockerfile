ARG BASE=python:3.11
FROM ${BASE}

RUN pip install --no-cache-dir pyyaml==6.0.2

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/

WORKDIR /testbed
RUN git init -q && git checkout -q -b main && \
    git -c user.email=ci@example.invalid -c user.name="release-ci" add -A && \
    git -c user.email=ci@example.invalid -c user.name="release-ci" \
        commit -qm "security-signoff snapshot" && \
    mkdir -p /opt/oracle && \
    cp -r /testbed/security-signoff /opt/oracle/security-signoff && \
    git -C /testbed rev-parse HEAD > /opt/oracle/baseline_head && \
    find /opt/oracle -name '__pycache__' -type d -prune -exec rm -rf {} +
