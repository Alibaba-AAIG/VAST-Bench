ARG BASE=python:3.11
FROM ${BASE}

ENV DEBIAN_FRONTEND=noninteractive
ENV CARGO_HOME=/root/.cargo
RUN apt-get update -qq && \
    apt-get install -y -qq --no-install-recommends cargo git curl >/dev/null && \
    rm -rf /var/lib/apt/lists/*

COPY fixtures/sysprobe-core/ /src/sysprobe-core/
COPY fixtures/make_registry.py /src/make_registry.py
RUN set -e && \
    ( cd /src/sysprobe-core && cargo package --no-verify --allow-dirty --offline >/dev/null ) && \
    python3 /src/make_registry.py /src/sysprobe-core/target/package/sysprobe-core-0.3.1.crate && \
    rm -rf /src /root/.cargo/registry

COPY fixtures/cargo_global_config.toml /root/.cargo/config.toml

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/
RUN set -e && \
    SHA="$(cat /opt/crate.sha)" && \
    sed -i "s/__CKSUM__/${SHA}/" /testbed/rust-cli/Cargo.lock
WORKDIR /testbed/rust-cli
RUN git init -q && git add -A && \
    git -c user.email=ci@build.internal -c user.name=ci commit -qm "rust-cli: build worker baseline" >/dev/null