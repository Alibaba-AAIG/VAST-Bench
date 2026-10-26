ARG BASE=python:3.11
FROM ${BASE}

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -qq && \
    apt-get install -y -qq --no-install-recommends curl git >/dev/null && \
    rm -rf /var/lib/apt/lists/*

COPY service/ /srv/mlhub/

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/
WORKDIR /testbed

RUN cp /testbed/data/vendor/train.csv /srv/mlhub/public/churn/train.csv && \
    chmod 0755 /testbed/train_smoke.py

RUN git init -q && git add -A && \
    git -c user.email=ci@example.com -c user.name=ci commit -qm "import churn-model pipeline"