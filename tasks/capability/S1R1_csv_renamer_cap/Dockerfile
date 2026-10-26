ARG BASE=python:3.11-slim
FROM ${BASE}
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*
COPY srv/ /srv/
COPY skill/ /srv/skill/
COPY tool/ /srv/tool/
COPY repo/ /testbed/
WORKDIR /testbed
