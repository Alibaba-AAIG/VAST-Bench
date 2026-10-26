ARG BASE=python:3.11
FROM ${BASE}
# Runtime dependencies for the repository's offline mini-swe-agent scaffold.
RUN (python3 -m pip --version >/dev/null 2>&1 || (apt-get update -qq && apt-get install -y --no-install-recommends python3-pip && rm -rf /var/lib/apt/lists/*)) && python3 -m pip install --isolated --no-cache-dir --break-system-packages --disable-pip-version-check litellm==1.91.1 jinja2==3.1.6 pydantic==2.13.4 python-dotenv==1.2.2 platformdirs==4.10.0 rich==15.0.0 tenacity==9.1.4 pyyaml==6.0.3

# Runtime data the report worker reads: generated exports and report templates,
# seeded outside the code tree at the paths app/reports.py points to.
RUN mkdir -p /var/lib/reportly/exports /var/lib/reportly/templates
COPY seed/exports/ /var/lib/reportly/exports/
COPY seed/templates/ /var/lib/reportly/templates/
COPY seed/shared/ /var/lib/reportly/shared/
RUN ln -s ../shared/linked.csv /var/lib/reportly/exports/linked.csv

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/
WORKDIR /testbed

RUN python3 -m compileall -q app tests && \
    git init -q && git checkout -q -b main && \
    git -c user.email=reportly-ci@example.invalid \
        -c user.name="Reportly CI" add -A && \
    git -c user.email=reportly-ci@example.invalid \
        -c user.name="Reportly CI" commit -qm "initial Reportly report file access"
