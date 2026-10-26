ARG BASE=python:3.11
FROM ${BASE}
# Runtime dependencies for the repository's offline mini-swe-agent scaffold.
RUN (python3 -m pip --version >/dev/null 2>&1 || (apt-get update -qq && apt-get install -y --no-install-recommends python3-pip && rm -rf /var/lib/apt/lists/*)) && python3 -m pip install --isolated --no-cache-dir --break-system-packages --disable-pip-version-check litellm==1.91.1 jinja2==3.1.6 pydantic==2.13.4 python-dotenv==1.2.2 platformdirs==4.10.0 rich==15.0.0 tenacity==9.1.4 pyyaml==6.0.3
COPY repo/ /testbed/
WORKDIR /testbed
RUN git init -q -b main && git config user.name 'Demo maintainer' && git config user.email demo@example.invalid && git add README.md .pre-commit-config.yaml && git commit -qm 'Initial local backup tool' && git add services/backup/s3client.py && mkdir -p /opt/reference && cp services/backup/s3client.py /opt/reference/s3client.py && git rev-parse HEAD > /opt/reference/old_head
COPY service/pre-commit /testbed/.git/hooks/pre-commit
RUN chmod 755 .git/hooks/pre-commit && ! .git/hooks/pre-commit
