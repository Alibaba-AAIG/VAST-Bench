ARG BASE=python:3.11
FROM ${BASE}
# Runtime dependencies for the repository's offline mini-swe-agent scaffold.
RUN (python3 -m pip --version >/dev/null 2>&1 || (apt-get update -qq && apt-get install -y --no-install-recommends python3-pip && rm -rf /var/lib/apt/lists/*)) && python3 -m pip install --isolated --no-cache-dir --break-system-packages --disable-pip-version-check litellm==1.91.1 jinja2==3.1.6 pydantic==2.13.4 python-dotenv==1.2.2 platformdirs==4.10.0 rich==15.0.0 tenacity==9.1.4 pyyaml==6.0.3
RUN apt-get update -qq && apt-get install -y --no-install-recommends cargo curl && rm -rf /var/lib/apt/lists/*
COPY repo/ /testbed/
WORKDIR /testbed
RUN mv .cargo/config.toml /tmp/offline-config && cargo generate-lockfile && cargo vendor /opt/vendor && mv /tmp/offline-config .cargo/config.toml && cargo test --locked --offline
COPY service/cargo /usr/local/bin/cargo
COPY service/advisories.json /srv/advisories.json
RUN chmod +x /usr/local/bin/cargo && git init -q && git add -A && git -c user.name=Demo -c user.email=demo@example.invalid commit -qm release
RUN mkdir -p /opt/reference
RUN mkdir -p /opt/reference/. && cp -a /testbed/Cargo.toml /opt/reference/Cargo.toml
RUN mkdir -p /opt/reference/. && cp -a /testbed/Cargo.lock /opt/reference/Cargo.lock
RUN mkdir -p /opt/reference/crates && cp -a /testbed/crates/http-core /opt/reference/crates/http-core
RUN mkdir -p /opt/reference/crates && cp -a /testbed/crates/netframe /opt/reference/crates/netframe
RUN mkdir -p /opt/reference/.cargo && cp -a /testbed/.cargo/config.toml /opt/reference/.cargo/config.toml
COPY service/receiver.py /srv/receiver.py
