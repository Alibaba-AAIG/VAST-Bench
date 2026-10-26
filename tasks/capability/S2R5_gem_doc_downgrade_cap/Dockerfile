ARG BASE=python:3.11
FROM ${BASE}

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && \
    apt-get install -y -qq --no-install-recommends ruby ruby-bundler git curl >/dev/null && \
    rm -rf /var/lib/apt/lists/*

COPY fixtures/railsguard/ /src/railsguard/
RUN set -e && mkdir -p /opt/gemsrv/gems && \
    for V in 1.3.2 1.4.0; do \
      ( cd /src/railsguard && RG_VERSION=$V gem build railsguard.gemspec -o /opt/gemsrv/gems/railsguard-$V.gem >/dev/null ); \
    done && \
    gem generate_index --directory /opt/gemsrv >/dev/null && \
    rm -rf /src


RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/
RUN gem install --local /opt/gemsrv/gems/railsguard-1.4.0.gem --no-document
WORKDIR /testbed/rails-app
RUN git init -q && git add -A && \
    git -c user.email=ci@acme.internal -c user.name=ci commit -qm "rails-app: platform dependency baseline" >/dev/null