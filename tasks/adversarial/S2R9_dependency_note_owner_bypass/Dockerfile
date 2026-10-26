ARG BASE=python:3.11-slim-bookworm
FROM ${BASE}
COPY dependency/notestore_sdk/ /usr/local/lib/python3.11/site-packages/notestore_sdk/
COPY repo/ /testbed/
ENV PYTHONPATH=/testbed/src
WORKDIR /testbed
RUN python3 -m compileall -q src tests && python3 -c "from notestore_sdk import Note, NoteStore"
