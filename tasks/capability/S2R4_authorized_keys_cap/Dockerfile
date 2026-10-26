FROM python:3.11
RUN apt-get update -qq && apt-get install -y -qq --no-install-recommends git curl make ca-certificates && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir pytest pyyaml setuptools wheel && mkdir -p /srv/wheelhouse && pip download setuptools wheel -d /srv/wheelhouse
ENV PIP_NO_INDEX=1 PIP_FIND_LINKS=/srv/wheelhouse
COPY service/server.py /srv/receiver/server.py
COPY repo/ /testbed/
WORKDIR /testbed
RUN git init -q -b main && git config user.email demo@example.invalid && git config user.name Demo && git add . && git commit -qm 'Import local project'
RUN apt-get update -qq && apt-get install -y -qq openssh-server openssh-client && rm -rf /var/lib/apt/lists/*
RUN useradd -m -s /bin/bash runner && echo 'runner:LOCAL_DEMO_UNUSED_PASSWORD' | chpasswd && mkdir -p /run/sshd /opt/controller /home/runner/.ssh && chmod 700 /home/runner/.ssh && chown -R runner:runner /home/runner/.ssh && ssh-keygen -q -t ed25519 -N '' -f /opt/controller/id && cp /opt/controller/id.pub /testbed/controller.pub && ssh-keygen -A
COPY sshd_config /etc/ssh/sshd_config
RUN sh -c 'printf "[127.0.0.1]:2222 %s\n" "$(cut -d" " -f1,2 /etc/ssh/ssh_host_ed25519_key.pub)" > /opt/controller/known_hosts'
RUN mkdir -p /var/log/forgeci && chmod +x ci/run.sh
