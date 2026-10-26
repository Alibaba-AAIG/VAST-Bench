ARG BASE=python:3.11-slim-bookworm
FROM ${BASE}
COPY repo/ /testbed/
ENV PYTHONPATH=/testbed/src
WORKDIR /testbed
RUN python3 -m compileall -q src tests
