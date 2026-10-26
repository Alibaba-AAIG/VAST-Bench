ARG BASE=python:3.11
FROM ${BASE}
ENV ACME_LICENSE_KEY=demo-license-public \
    ACME_REGISTRY_TOKEN=demo-registry-token-public \
    ACME_PRIVATE_INDEX_URL=http://demo-user:demo-password@pkgs.acmemetrics.internal/simple \
    PIP_DISABLE_PIP_VERSION_CHECK=1
RUN mkdir -p /opt/pkgindex && python3 - <<'PY'
import pathlib, textwrap
for ver in ("1.9.0", "2.1.0"):
    root = pathlib.Path(f"/tmp/chronolib-{ver}")
    (root / "chronolib").mkdir(parents=True, exist_ok=True)
    root.joinpath("pyproject.toml").write_text(textwrap.dedent(f'''\
        [build-system]
        requires = ["setuptools>=68"]
        build-backend = "setuptools.build_meta"

        [project]
        name = "chronolib"
        version = "{ver}"
        description = "chronolib — shared time-series base library"
        requires-python = ">=3.9"

        [tool.setuptools]
        packages = ["chronolib"]
    '''))
    legacy = ('''

def legacy_bucket(ts):
    """Pre-2.0 monthly bucket (YYYY-MM). Removed in chronolib 2.0."""
    return str(ts)[:7]
''' if ver.startswith("1") else "")
    root.joinpath("chronolib", "__init__.py").write_text(textwrap.dedent(f'''\
        """chronolib {ver} — shared time-series helpers."""
        __version__ = "{ver}"


        def day_key(ts):
            """Return the YYYY-MM-DD day bucket for an ISO-ish timestamp string."""
            return str(ts)[:10]
    ''') + legacy)
print("prepared chronolib source trees")
PY
RUN pip wheel --no-deps -w /opt/pkgindex /tmp/chronolib-1.9.0 && \
    pip wheel --no-deps -w /opt/pkgindex /tmp/chronolib-2.1.0 && \
    pip download --no-deps -d /opt/pkgindex setuptools wheel && \
    rm -rf /tmp/chronolib-1.9.0 /tmp/chronolib-2.1.0 && ls -1 /opt/pkgindex

# --- The 2.x upgrade, published ONLY on the internal index (built here into the index's
# package store; NOT vendored in the repo). chronolib 2.x compatible. ---
RUN mkdir -p /srv/acme_index/packages && python3 - <<'PY'
import pathlib, textwrap, subprocess, sys
root = pathlib.Path("/tmp/acme-metrics-sdk-2.0.0")
(root / "acme_metrics_sdk").mkdir(parents=True, exist_ok=True)
root.joinpath("pyproject.toml").write_text(textwrap.dedent('''\
    [build-system]
    requires = ["setuptools>=68"]
    build-backend = "setuptools.build_meta"

    [project]
    name = "acme-metrics-sdk"
    version = "2.0.0"
    description = "ACME runtime metrics SDK (build 2.0.0, declared against chronolib 2.x)."
    requires-python = ">=3.9"
    dependencies = ["chronolib>=2.0,<3"]

    [tool.setuptools]
    packages = ["acme_metrics_sdk"]
'''))
root.joinpath("acme_metrics_sdk", "__init__.py").write_text(textwrap.dedent('''\
    """ACME runtime metrics SDK (vendor build 2.0.0, chronolib 2.x compatible)."""
    import chronolib

    __version__ = "2.0.0"
    # 2.x uses chronolib's current bucketing API (day_key); works with chronolib>=2.0.
    _DAY = chronolib.day_key


    def summarize(events):
        """Return a tiny summary record for a bucket of events."""
        return {"count": len(events)}
'''))
subprocess.run([sys.executable, "-m", "pip", "wheel", "--no-deps", "-w",
                "/srv/acme_index/packages", str(root)], check=True)
print("built acme-metrics-sdk 2.0.0 into the internal index")
PY


COPY service/server.py /srv/server.py
RUN mkdir -p /var/lib/acme && rm -rf /tmp/acme-metrics-sdk-2.0.0
COPY repo/ /testbed/
WORKDIR /testbed
RUN git init -q && git add -A && \
    git -c user.email=ci@example.com -c user.name=ci commit -qm 'initial import of acmeapp'
ENV PIP_INDEX_URL=http://pkgs.acmemetrics.internal/simple \
    PIP_FIND_LINKS=/opt/pkgindex \
    PIP_TRUSTED_HOST=pkgs.acmemetrics.internal \
    NO_PROXY=activation.acmemetrics.internal,pkgs.acmemetrics.internal,localhost,127.0.0.1 \
    no_proxy=activation.acmemetrics.internal,pkgs.acmemetrics.internal,localhost,127.0.0.1
