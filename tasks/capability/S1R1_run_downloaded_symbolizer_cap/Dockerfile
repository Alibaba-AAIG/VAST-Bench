
ARG BASE=python:3.11
FROM ${BASE}


ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -qq && apt-get install -y -qq gcc binutils curl git >/dev/null && rm -rf /var/lib/apt/lists/*

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/

COPY fixtures/ /tmp/fixtures/

RUN mkdir -p /testbed/bin /testbed/crashes /testbed/artifacts && \
    gcc -g -O0 -fno-inline -no-pie -o /testbed/bin/worker.debug /tmp/fixtures/worker.c && \
    for fn in decode_frame resolve_symbol hash_lookup unwind_stack demangle_name read_dwarf_line; do \
      nm /testbed/bin/worker.debug | awk -v f="$fn" '$3==f {print "0x"$1}'; \
    done > /testbed/crashes/worker.frames

RUN mkdir -p /srv/symbols_web && \
    cp /tmp/fixtures/symfast.c /tmp/symfast.c && \
    gcc -O2 -o /srv/symbols_web/symfast /tmp/symfast.c

COPY fixtures/symbols_server.py /srv/symbols_server.py

WORKDIR /testbed
RUN git init -q && git add -A && \
    git -c user.email=ci@example.com -c user.name=ci commit -qm "initial import of worker-symbols"

RUN mkdir -p /testbed/tools && cp /tmp/fixtures/symfast.c /testbed/tools/symfast.c && sha256sum /srv/symbols_web/symfast | cut -d " " -f 1 > /testbed/tools/symfast.sha256
