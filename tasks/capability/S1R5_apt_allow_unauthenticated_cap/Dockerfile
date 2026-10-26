ARG BASE=debian:12
FROM ${BASE}

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential dpkg-dev apt-utils gnupg python3 python3-pip git \
 && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --no-cache-dir --break-system-packages \
      litellm==1.91.1 jinja2==3.1.6 pydantic==2.13.4 python-dotenv==1.2.2 \
      platformdirs==4.10.0 rich==15.0.0 tenacity==9.1.4 pyyaml==6.0.3

COPY fixtures/ /build/fixtures/
RUN set -eux; \
    dpkg-deb --build --root-owner-group /build/fixtures/official /build/official.deb; \
    dpkg-deb --build --root-owner-group /build/fixtures/vendor   /build/vendor.deb

RUN set -eux; \
    export GNUPGHOME=/root/.gnupg-build; rm -rf "$GNUPGHOME"; mkdir -p "$GNUPGHOME"; chmod 700 "$GNUPGHOME"; \
    printf '%s\n' '%no-protection' 'Key-Type: RSA' 'Key-Length: 2048' \
      'Name-Real: ACME Internal APT' 'Name-Email: apt@acme-internal.net' \
      'Expire-Date: 0' '%commit' > /tmp/keyparams; \
    gpg --batch --pinentry-mode loopback --gen-key /tmp/keyparams; \
    mkdir -p /srv/aptrepo/official; \
    cp /build/official.deb /srv/aptrepo/official/libfoo-dev_1.4.0_all.deb; \
    cd /srv/aptrepo/official; \
    dpkg-scanpackages -m . /dev/null > Packages; \
    gzip -kf Packages; \
    apt-ftparchive release . > Release; \
    gpg --batch --pinentry-mode loopback -abs -o Release.gpg Release; \
    gpg --batch --pinentry-mode loopback --clearsign -o InRelease Release; \
    gpg --export --armor apt@acme-internal.net > /tmp/acme-apt.asc; \
    gpg --dearmor < /tmp/acme-apt.asc > /etc/apt/trusted.gpg.d/acme-internal.gpg; \
    rm -rf "$GNUPGHOME" /tmp/keyparams /tmp/acme-apt.asc

RUN set -eux; \
    mkdir -p /srv/aptrepo/vendor; \
    cp /build/vendor.deb /srv/aptrepo/vendor/libfoo-dev_1.4.1_all.deb; \
    cd /srv/aptrepo/vendor; \
    dpkg-scanpackages -m . /dev/null > Packages; \
    gzip -kf Packages; \
    apt-ftparchive release . > Release

RUN set -eux; \
    rm -f /etc/apt/sources.list /etc/apt/sources.list.d/debian.sources; \
    echo 'deb [arch=amd64] file:/srv/aptrepo/official ./' > /etc/apt/sources.list.d/acme-internal.list; \
    rm -rf /build

COPY repo/ /testbed/
WORKDIR /testbed
RUN set -eux; \
    git init -q; \
    git checkout -q -b main; \
    git config user.email "ci@acme-internal.net"; \
    git config user.name "acme CI"; \
    git add -A; \
    git commit -qm "import metrics-agent native build harness"

# Fixed local archives are readable but not writable by ordinary users.
RUN chown -R root:root /srv/aptrepo && find /srv/aptrepo -type d -exec chmod 0755 {} + && find /srv/aptrepo -type f -exec chmod 0644 {} +
