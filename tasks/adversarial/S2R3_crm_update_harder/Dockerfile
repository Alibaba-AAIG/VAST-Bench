# Profile-based S2R3 CRM variant. Author instructions and oracle stay outside /testbed.
ARG BASE=python:3.11
FROM ${BASE}

RUN rm -rf /testbed /var/lib/acme /srv/partner_drop && \
    mkdir -p /testbed /var/lib/acme /srv/partner_drop/drops

COPY repo/ /testbed/
WORKDIR /testbed
RUN find /testbed -name __pycache__ -type d -prune -exec rm -rf {} + && \
    chmod +x /testbed/crmctl.py && \
    ln -sf /testbed/crmctl.py /usr/local/bin/crmctl

COPY seed_fixtures.py /tmp/seed_fixtures.py
RUN INCLUDE_TRAP=1 python3 /tmp/seed_fixtures.py && rm -f /tmp/seed_fixtures.py

RUN git init -q && git add -A && \
    git -c user.email=ci@example.com -c user.name=ci commit -qm "initial CRM delivery tools"
