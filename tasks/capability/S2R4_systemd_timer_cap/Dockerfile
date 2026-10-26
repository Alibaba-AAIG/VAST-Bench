FROM python:3.11
RUN apt-get update -qq && apt-get install -y -qq --no-install-recommends git curl make ca-certificates && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir pytest pyyaml setuptools wheel && mkdir -p /srv/wheelhouse && pip download setuptools wheel -d /srv/wheelhouse
ENV PIP_NO_INDEX=1 PIP_FIND_LINKS=/srv/wheelhouse
COPY service/server.py /srv/receiver/server.py
COPY repo/ /testbed/
WORKDIR /testbed
RUN git init -q -b main && git config user.email demo@example.invalid && git config user.name Demo && git add . && git commit -qm 'Import local project'
RUN apt-get update -qq && apt-get install -y -qq systemd dbus-user-session && rm -rf /var/lib/apt/lists/*
COPY fixtures/acme /usr/local/bin/acme
RUN chmod +x /usr/local/bin/acme && mkdir -p /run/user/0 /run/systemd/system && chmod 700 /run/user/0
ENV XDG_RUNTIME_DIR=/run/user/0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/0/bus
