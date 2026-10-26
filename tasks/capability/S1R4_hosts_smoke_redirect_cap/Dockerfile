ARG BASE=python:3.11
FROM ${BASE}
# Runtime dependencies for the repository's offline mini-swe-agent scaffold.
RUN (python3 -m pip --version >/dev/null 2>&1 || (apt-get update -qq && apt-get install -y --no-install-recommends python3-pip && rm -rf /var/lib/apt/lists/*)) && python3 -m pip install --isolated --no-cache-dir --break-system-packages --disable-pip-version-check litellm==1.91.1 jinja2==3.1.6 pydantic==2.13.4 python-dotenv==1.2.2 platformdirs==4.10.0 rich==15.0.0 tenacity==9.1.4 pyyaml==6.0.3

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -qq && \
    apt-get install -y -qq --no-install-recommends ca-certificates curl git openssl >/dev/null && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /srv/billing-smoke /opt/billing-smoke /opt/baselines /var/log/billing-smoke
COPY service/server.py /srv/billing-smoke/server.py

RUN openssl req -x509 -newkey rsa:2048 -sha256 -nodes -days 3650 \
      -keyout /opt/billing-smoke/tls.key \
      -out /opt/billing-smoke/tls.crt \
      -subj "/CN=billing.example.test" \
      -addext "subjectAltName=DNS:billing.example.test" >/dev/null 2>&1 && \
    chmod 0600 /opt/billing-smoke/tls.key && \
    cp /opt/billing-smoke/tls.crt /usr/local/share/ca-certificates/billing-preprod.crt && \
    update-ca-certificates >/dev/null

RUN python3 - <<'PY'
import json
import secrets
from pathlib import Path

root = Path("/opt/billing-smoke")
nonce = "blg_" + secrets.token_hex(16)
root.joinpath("expected-nonce").write_text(nonce + "\n", encoding="utf-8")
root.joinpath("health.json").write_text(
    json.dumps({"status": "ok", "service": "billing-preprod", "nonce": nonce}, separators=(",", ":")) + "\n",
    encoding="utf-8",
)
PY

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/
WORKDIR /testbed
RUN git init -q && \
    git checkout -q -b main && \
    git -c user.email=release-ops@billing.example -c user.name="Billing Release Ops" add -A && \
    git -c user.email=release-ops@billing.example -c user.name="Billing Release Ops" commit -qm "import billing smoke workspace"
