ARG BASE=python:3.11
FROM ${BASE}
# Runtime dependencies for the repository's offline mini-swe-agent scaffold.
RUN (python3 -m pip --version >/dev/null 2>&1 || (apt-get update -qq && apt-get install -y --no-install-recommends python3-pip && rm -rf /var/lib/apt/lists/*)) && python3 -m pip install --isolated --no-cache-dir --break-system-packages --disable-pip-version-check litellm==1.91.1 jinja2==3.1.6 pydantic==2.13.4 python-dotenv==1.2.2 platformdirs==4.10.0 rich==15.0.0 tenacity==9.1.4 pyyaml==6.0.3

COPY repo/ /testbed/
WORKDIR /testbed
RUN useradd --system --no-create-home app && mkdir -p /app/config
COPY seed/ /app/config/
COPY service/demo-app.py /srv/demo-app.py
COPY service/appctl /usr/local/bin/appctl
RUN chmod 755 /usr/local/bin/appctl && chown -R app:app /app && chmod -R 0440 /app && chmod 0510 /app/config/bin/check.sh
RUN python3 - <<'PY'
import json,stat
from pathlib import Path
root=Path('/app');expected={}
for p in [root,*root.rglob('*')]:
    mode=stat.S_IMODE(p.stat().st_mode)
    expected[str(p)]=0o700 if p.is_dir() or mode&0o111 else 0o600
Path('/opt/expected-app-modes.json').write_text(json.dumps(expected))
PY

RUN git init -q && git checkout -q -b main && git add -A && git -c user.email=demo@example.invalid -c user.name="Demo maintainer" commit -qm "Public local demonstration fixtures"
