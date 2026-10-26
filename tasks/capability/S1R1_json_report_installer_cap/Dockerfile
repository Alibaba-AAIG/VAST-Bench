ARG BASE=python:3.11-slim
FROM ${BASE}
RUN apt-get update && apt-get install -y --no-install-recommends bash curl \
    && rm -rf /var/lib/apt/lists/*
ENV NO_PROXY=get.reportforge.test,localhost,127.0.0.1 \
    no_proxy=get.reportforge.test,localhost,127.0.0.1
COPY service/ /srv/reportforge/
COPY repo/ /testbed/
WORKDIR /testbed
