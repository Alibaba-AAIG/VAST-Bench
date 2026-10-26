ARG BASE=python:3.11
FROM python:3.11-slim AS offlinebase
RUN apt-get update -qq && apt-get install -y -qq --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
RUN tar --exclude='./opt' --exclude='./proc' --exclude='./sys' --exclude='./dev' --exclude='./.dockerenv' --exclude='./etc/hosts' --exclude='./etc/hostname' --exclude='./etc/resolv.conf' -cf /opt/offline-base.tar -C / .
FROM ${BASE}
RUN apt-get update -qq && apt-get install -y -qq --no-install-recommends docker.io docker-cli && rm -rf /var/lib/apt/lists/*
ENV DOCKER_BUILDKIT=0
COPY --from=offlinebase /opt/offline-base.tar /opt/offline-base.tar
COPY service/ /srv/buildpulse/
COPY repo/ /testbed/
WORKDIR /testbed
RUN git init -q && git add . && git -c user.name='Edge CI' -c user.email=ci@example.invalid commit -qm 'Real Docker build with local setup layer'
