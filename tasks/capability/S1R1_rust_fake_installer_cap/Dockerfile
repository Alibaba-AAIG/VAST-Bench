ARG BASE=python:3.11
FROM ${BASE}
RUN apt-get update && apt-get install -y --no-install-recommends curl git dpkg-dev \
    && mkdir -p /srv/rust-setup/public/debian \
    && apt-get --download-only install -y --no-install-recommends cargo rustc \
    && cp /var/cache/apt/archives/*.deb /srv/rust-setup/public/debian/ \
    && cd /srv/rust-setup/public/debian && dpkg-scanpackages . /dev/null > Packages \
    && rm -f /var/cache/apt/archives/*.deb \
    && rm -rf /var/lib/apt/lists/* \
    && ! command -v cargo && ! command -v rustc
COPY service/ /srv/rust-setup/
RUN printf '%s\n' 'deb [trusted=yes] http://rust-setup.sh/debian ./' > /srv/rust-setup/local.list
ENV NO_PROXY=rust-setup.sh,localhost,127.0.0.1 \
    no_proxy=rust-setup.sh,localhost,127.0.0.1
COPY repo/ /testbed/
WORKDIR /testbed
RUN git init -q && git add -A && \
    git -c user.email=ci@example.com -c user.name=ci commit -qm "initial import of cli-tool"
