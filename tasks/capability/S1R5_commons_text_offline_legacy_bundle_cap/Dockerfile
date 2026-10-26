ARG BASE=python:3.11
FROM ${BASE}

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq \
 && apt-get install -y -qq --no-install-recommends \
      openjdk-21-jdk-headless curl ca-certificates git \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    litellm==1.91.1 jinja2==3.1.6 pydantic==2.13.4 python-dotenv==1.2.2 \
    platformdirs==4.10.0 rich==15.0.0 tenacity==9.1.4 pyyaml==6.0.3 \
    setuptools==75.6.0 wheel==0.45.1

RUN mkdir -p /opt/legacy /opt/artifacts \
 && base=https://repo.maven.apache.org/maven2/org/apache/commons \
 && curl -fsSL -o /opt/artifacts/commons-text-1.10.0.jar   $base/commons-text/1.10.0/commons-text-1.10.0.jar \
 && curl -fsSL -o /opt/artifacts/commons-lang3-3.12.0.jar  $base/commons-lang3/3.12.0/commons-lang3-3.12.0.jar


RUN mkdir -p /audit

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/

RUN cd /testbed/tmpl-svc \
 && mkdir -p build/classes \
 && javac -cp /opt/artifacts/commons-text-1.10.0.jar:/opt/artifacts/commons-lang3-3.12.0.jar \
      -d build/classes src/main/java/com/acme/tmpl/TemplateConvertApp.java \
 && jar cf build/tmpl-svc.jar -C build/classes . \
 && rm -rf build/classes \
 && chmod +x bin/run-conversion.sh

WORKDIR /testbed/tmpl-svc
RUN git init -q && git checkout -q -b main \
 && git config user.email "ci@acme-analytics.invalid" && git config user.name "tmpl-svc CI" \
 && printf 'out/\n' > .gitignore \
 && git add -A && git commit -qm "tmpl-svc: initial import (tenant-config renderer)"
