ARG BASE=python:3.11
FROM ${BASE}
RUN pip install --no-cache-dir cryptography==43.0.1
COPY repo/ /testbed/
COPY fixtures/build_inputs.py /opt/build_inputs.py
WORKDIR /testbed
RUN python3 /opt/build_inputs.py && rm /opt/build_inputs.py && chmod +x scripts/* && git init -q && git add . && git -c user.name='Fixture CI' -c user.email=ci@example.invalid commit -qm 'Current upstream handoff inputs'
