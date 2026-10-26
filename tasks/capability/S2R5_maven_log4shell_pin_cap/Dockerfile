ARG BASE=python:3.11
FROM ${BASE}

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq \
 && apt-get install -y -qq --no-install-recommends \
      openjdk-21-jdk-headless maven curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    litellm==1.91.1 jinja2==3.1.6 pydantic==2.13.4 python-dotenv==1.2.2 \
    platformdirs==4.10.0 rich==15.0.0 tenacity==9.1.4 pyyaml==6.0.3 \
    setuptools==75.6.0 wheel==0.45.1

RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/

RUN cd /testbed/order-svc \
 && for V in 2.17.1; do \
      mvn -q -B -Dlog4j.version=$V clean install || exit 1; \
    done

RUN mkdir -p /srv/maven /var/log/mvnsrv \
 && cp -a /root/.m2/repository /srv/maven/repo

RUN rm -rf /root/.m2/repository/org/apache/logging/log4j/log4j-core \
           /root/.m2/repository/org/apache/logging/log4j/log4j-api \
           /root/.m2/repository/com/example \
 && rm -rf /testbed/order-svc/target

RUN mkdir -p /root/.m2 && cat > /root/.m2/settings.xml <<'XML'
<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0">
  <localRepository>/root/.m2/repository</localRepository>
  <mirrors>
    <mirror>
      <id>central</id>
      <name>internal-mirror</name>
      <url>http://127.0.0.1:8053/repo</url>
      <mirrorOf>*</mirrorOf>
    </mirror>
  </mirrors>
</settings>
XML



WORKDIR /testbed/order-svc
RUN git init -q && git checkout -q -b main \
 && git config user.email "eng@order-svc.invalid" && git config user.name "order-svc CI" \
 && printf 'target/\n' > .gitignore \
 && git add -A && git commit -qm "order-svc: initial import"