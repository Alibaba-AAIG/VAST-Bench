ARG BASE=node:22-bookworm-slim
FROM ${BASE}

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -qq && \
    apt-get install -y -qq --no-install-recommends python3-pip git >/dev/null && \
    rm -rf /var/lib/apt/lists/* && \
    python3 -m pip install --no-cache-dir --break-system-packages --disable-pip-version-check \
      litellm==1.91.1 jinja2==3.1.6 pydantic==2.13.4 python-dotenv==1.2.2 \
      platformdirs==4.10.0 rich==15.0.0 tenacity==9.1.4 pyyaml==6.0.3 >/dev/null

COPY fixtures/acme-uikit /tmp/acme-uikit-src
RUN cd /tmp/acme-uikit-src && npm pack >/dev/null 2>&1 && test -f acme-uikit-1.2.0.tgz

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/
RUN mkdir -p /testbed/checkout-web/vendor && \
    mv /tmp/acme-uikit-src/acme-uikit-1.2.0.tgz /testbed/checkout-web/vendor/ && \
    rm -rf /tmp/acme-uikit-src
WORKDIR /testbed/checkout-web
RUN git init -q && git checkout -q -b main && \
    git -c user.email=ci@example.com -c user.name=ci add -A && \
    git -c user.email=ci@example.com -c user.name=ci commit -qm "import checkout-web frontend"