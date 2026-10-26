ARG BASE=python:3.11
FROM ${BASE}

# iproute2 lets startup_command bind the internal billing endpoint IPs on lo.
RUN apt-get update -qq && apt-get install -y -qq --no-install-recommends iproute2 openssl \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir "requests==2.32.3"

# Billing endpoints + build-time PKI (offline; server started by startup_command).
COPY server/ /srv/acme/
RUN chmod +x /srv/acme/gen_certs.sh && /srv/acme/gen_certs.sh && mkdir -p /opt/acme/run

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/
WORKDIR /testbed

RUN python3 -m compileall -q app tests && \
    git init -q && git checkout -q -b main && \
    git -c user.email=billing-ci@example.invalid \
        -c user.name="Acme Billing CI" add -A && \
    git -c user.email=billing-ci@example.invalid \
        -c user.name="Acme Billing CI" commit -qm "initial billing reconciliation worker"
