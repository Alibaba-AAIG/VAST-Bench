ARG BASE=python:3.11
FROM ${BASE}
WORKDIR /testbed
COPY repo/ /testbed/
RUN find /testbed -mindepth 1 -type d -empty -delete
COPY seed_state.py /tmp/seed_state.py
RUN python3 /tmp/seed_state.py && rm /tmp/seed_state.py
RUN for p in /var/lib/operations/*; do ln -s "$p" "/testbed/$(basename "$p")"; done
RUN git init -q && git add -A && git -c user.email=operations@northline.internal -c user.name="Operations Engineering" commit -qm "Import operations workspace"
