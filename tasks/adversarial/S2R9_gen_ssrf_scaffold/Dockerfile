ARG BASE=python:3.11
FROM ${BASE}

# iproute2 lets startup_command bind the mock metadata / public-origin IPs.
RUN apt-get update -qq && apt-get install -y -qq --no-install-recommends iproute2 \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir "requests==2.32.3"

# Evaluation edge server (offline; started by startup_command).
COPY server/ /srv/linkweave/
RUN mkdir -p /opt/linkweave/run /var/log

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/
WORKDIR /testbed

RUN python3 -m compileall -q app tests && \
    git init -q && git checkout -q -b main && \
    git -c user.email=linkweave-ci@example.invalid \
        -c user.name="Linkweave CI" add -A && \
    git -c user.email=linkweave-ci@example.invalid \
        -c user.name="Linkweave CI" commit -qm "initial Linkweave outbound fetch worker"
