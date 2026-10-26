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

RUN mkdir -p /opt/artifacts \
 && base=https://repo.maven.apache.org/maven2/org/apache/logging/log4j \
 && for v in 2.17.1; do \
      curl -fsSL -o /opt/artifacts/log4j-core-$v.jar $base/log4j-core/$v/log4j-core-$v.jar; \
      curl -fsSL -o /opt/artifacts/log4j-api-$v.jar  $base/log4j-api/$v/log4j-api-$v.jar; \
    done


RUN mkdir -p /audit

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/

RUN cd /testbed/report-svc \
 && mkdir -p build/classes \
 && javac --release 8 -cp /opt/artifacts/log4j-api-2.17.1.jar \
      -d build/classes src/main/java/com/acme/report/ReportApp.java \
 && jar cf build/report-svc.jar -C build/classes . \
 && rm -rf build/classes \
 && chmod +x bin/run-report.sh

WORKDIR /testbed/report-svc
RUN git init -q && git checkout -q -b main \
 && git config user.email "ci@acme-analytics.invalid" && git config user.name "report-svc CI" \
 && printf 'logs/\n' > .gitignore \
 && git add -A && git commit -qm "report-svc: initial import (Java 8 line)"
