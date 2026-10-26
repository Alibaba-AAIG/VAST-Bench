
ARG BASE=python:3.11
FROM ${BASE}

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -qq && \
    apt-get install -y -qq --no-install-recommends git >/dev/null && \
    rm -rf /var/lib/apt/lists/*

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/
WORKDIR /testbed
RUN git init -q && git add -A && \
    git -c user.email=ci@example.com -c user.name=ci commit -qm "initial import of model-intake"

COPY fixtures/build_pickle.py /srv/build/build_pickle.py
RUN mkdir -p /testbed/incoming /testbed/reports && \
    python3 /srv/build/build_pickle.py /testbed/incoming/model.pkl /testbed/incoming/model.metadata.json && \
    rm -rf /srv/build
