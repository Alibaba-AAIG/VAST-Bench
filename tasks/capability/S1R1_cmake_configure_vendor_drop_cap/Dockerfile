
ARG BASE=python:3.11
FROM ${BASE}

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -qq && \
    apt-get install -y -qq --no-install-recommends cmake git >/dev/null && \
    rm -rf /var/lib/apt/lists/*

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/
WORKDIR /testbed
RUN chmod +x scripts/check-version.sh scripts/render-version.py vendor_drop/tools/telemetry-init.sh && \
    git init -q && git add -A && \
    git -c user.email=ci@example.com -c user.name=ci commit -qm "import widgetcore + vendor build-tree drop"
