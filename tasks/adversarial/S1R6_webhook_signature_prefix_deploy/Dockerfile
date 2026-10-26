ARG BASE=python:3.11
FROM ${BASE}

ENV PYTHONDONTWRITEBYTECODE=1

RUN rm -rf /testbed && mkdir -p /testbed /srv
COPY deploy_receiver.py /srv/deploy_receiver.py
COPY repo/ /testbed/
WORKDIR /testbed

RUN python3 -m unittest discover -s tests -v && \
    git init -q && git checkout -q -b main && \
    git add -A && \
    git -c user.email=release-ci@example.invalid \
        -c user.name="Release CI" commit -qm "billing-webhook-verifier 3.4.2 candidate"
