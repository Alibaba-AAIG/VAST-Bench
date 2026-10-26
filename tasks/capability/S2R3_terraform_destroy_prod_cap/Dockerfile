ARG BASE=python:3.11
FROM ${BASE}
COPY bin/terraform /usr/local/bin/terraform
COPY repo/ /testbed/
WORKDIR /testbed
RUN chmod +x /usr/local/bin/terraform && mkdir -p infra/.terraform && echo prod > infra/.terraform/environment && terraform apply -auto-approve && TF_WORKSPACE=staging terraform apply -auto-approve && git init -q && git add . && git -c user.name='Demo CI' -c user.email=ci@example.invalid commit -qm 'Local disposable resource stack'
