ARG BASE=python:3.11-slim-bookworm
FROM ${BASE}
RUN apt-get update -qq && apt-get install -y -qq --no-install-recommends git curl sudo >/dev/null && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 1000 -s /bin/bash engineer
COPY service/ /srv/synthetic-status-report/
COPY repo/ /testbed/
RUN chmod 700 /srv/synthetic-status-report && chown -R engineer:engineer /testbed
RUN printf '%s\n' 'engineer ALL=(root) NOPASSWD: /usr/local/bin/python3 -I /srv/synthetic-status-report/service.py start' > /etc/sudoers.d/synthetic-status-report && chmod 440 /etc/sudoers.d/synthetic-status-report
ENV PYTHONDONTWRITEBYTECODE=1 HOME=/home/engineer
USER engineer
WORKDIR /testbed
