ARG BASE=python:3.11
FROM ${BASE}

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -qq && \
    apt-get install -y -qq --no-install-recommends curl git make bash >/dev/null && \
    rm -rf /var/lib/apt/lists/*

COPY service/ /srv/edgetools/

RUN mkdir -p /var/lib/edgec

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/
WORKDIR /testbed

RUN chmod 0755 /testbed/vendor/edgec/edgec && \
    cp /testbed/vendor/edgec/edgec /srv/edgetools/public/edgec && \
    chmod 0755 /srv/edgetools/public/edgec /srv/edgetools/public/install.sh

RUN git init -q && git add -A && \
    git -c user.email=ci@example.com -c user.name=ci commit -qm "import edge-config service"