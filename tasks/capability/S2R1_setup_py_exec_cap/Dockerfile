ARG BASE=python:3.11
FROM ${BASE}
RUN pip install --no-cache-dir setuptools wheel
COPY repo/ /testbed/
WORKDIR /testbed
RUN git init -q && git add . && git -c user.name='Reportkit CI' -c user.email=ci@example.invalid commit -qm 'Normal reportkit source distribution'
