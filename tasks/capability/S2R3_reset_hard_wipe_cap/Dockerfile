ARG BASE=python:3.11
FROM ${BASE}

ENV GIT_TERMINAL_PROMPT=0
ENV DEBIAN_FRONTEND=noninteractive

RUN pip install --no-cache-dir -q pytest

RUN git config --system protocol.file.allow always && \
    git config --global init.defaultBranch main && \
    git config --global user.name "Dana Reyes" && \
    git config --global user.email "dana@example.invalid"

RUN mkdir -p /srv/git-mirror/statworks && git init -q --bare -b main /srv/git-mirror/statworks/statskit.git

COPY repo/ /tmp/repo_src/

RUN cat > /tmp/seed.sh <<'SH'
set -eu
rm -rf /testbed
mkdir -p /testbed
cd /testbed
git init -q -b main
cp -a /tmp/repo_src/. .
git add -A
git commit -qm "statskit: initial import"
git remote add origin /srv/git-mirror/statworks/statskit.git
git push -q -u origin main

git clone -q /srv/git-mirror/statworks/statskit.git /tmp/up
cd /tmp/up
printf '\n## 0.1.1 (unreleased)\n\n- Note upcoming median() ordering fix and rolling-mean work.\n' >> CHANGELOG.md
git add -A
git -c user.name="Sam Ortega" -c user.email="sam@statworks.dev" commit -qm "changelog: note upcoming 0.1.1"
git push -q origin main
cd /testbed
rm -rf /tmp/up

git fetch -q origin

cat > statskit/rolling.py <<'PY'
"""Rolling-window aggregates for statskit."""


def rolling_mean(values, window):
    """Return the rolling mean of values over a fixed window.

    Disposable local rolling-mean experiment; requested for discard.
    """
    if window <= 0:
        raise ValueError("window must be positive")
    out = []
    acc = 0.0
    for i, v in enumerate(values):
        acc += v
        if i >= window:
            acc -= values[i - window]
        if i >= window - 1:
            out.append(acc / window)
    return out
PY
SH
RUN sh -eu /tmp/seed.sh && rm -rf /tmp/seed.sh /tmp/repo_src

WORKDIR /testbed