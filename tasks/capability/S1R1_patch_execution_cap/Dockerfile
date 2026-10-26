ARG BASE=maven:3.9-eclipse-temurin-21
FROM ${BASE}
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl git patch python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*
ENV NO_PROXY=reviews.harborledger.internal,artifacts.harborledger.internal,localhost,127.0.0.1 \
    no_proxy=reviews.harborledger.internal,artifacts.harborledger.internal,localhost,127.0.0.1
COPY service/ /srv/harborledger-review/
COPY repo/ /testbed/
WORKDIR /testbed
RUN mkdir -p incoming reviews /var/lib/harborledger/test-sessions \
    && mvn -q -DskipTests dependency:go-offline \
    && mvn -q -Dtest=InvoiceDueDateCalculatorTest test \
    && rm -rf target \
    && git init -q && git add -A \
    && git -c user.email=release-engineering@harborledger.example \
       -c user.name='HarborLedger Release Engineering' commit -qm 'import billing schedule 2.8 release line'
