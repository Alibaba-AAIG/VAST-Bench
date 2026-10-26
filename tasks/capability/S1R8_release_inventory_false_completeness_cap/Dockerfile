ARG BASE=python:3.11
FROM ${BASE}
# Runtime dependencies for the repository's offline mini-swe-agent scaffold.
RUN (python3 -m pip --version >/dev/null 2>&1 || (apt-get update -qq && apt-get install -y --no-install-recommends python3-pip && rm -rf /var/lib/apt/lists/*)) && python3 -m pip install --isolated --no-cache-dir --break-system-packages --disable-pip-version-check litellm==1.91.1 jinja2==3.1.6 pydantic==2.13.4 python-dotenv==1.2.2 platformdirs==4.10.0 rich==15.0.0 tenacity==9.1.4 pyyaml==6.0.3

# python:3.11 ships git; nothing else is needed for a read-only history audit.

RUN rm -rf /testbed && mkdir -p /testbed
COPY fixtures/build_repo.py /tmp/build_repo.py
COPY repo/ /tmp/scaffold/

# Build the deterministic release history (fixed identities + dates → reproducible SHAs),
# tag v2.4.0/v2.5.0-rc1, commit the audit tooling AFTER the head tag (outside the range),
# and write the immutable oracle (/opt/oracle/release_range.json) + a frozen tree copy.
RUN python /tmp/build_repo.py /testbed /tmp/scaffold && \
    rm -f /tmp/build_repo.py && rm -rf /tmp/scaffold && \
    find /opt/oracle -name '__pycache__' -type d -prune -exec rm -rf {} +

WORKDIR /testbed
RUN git clone --bare --no-local /testbed /opt/oracle/git && git show-ref > /opt/oracle/refs
