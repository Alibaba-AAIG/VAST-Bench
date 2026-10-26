ARG BASE=python:3.11-slim-bookworm
FROM ${BASE}

COPY repo/ /testbed/
COPY release_receiver.py /srv/release_receiver.py
ENV PYTHONPATH=/testbed/src
WORKDIR /testbed
RUN python3 -m compileall -q src tools tests /srv/release_receiver.py
