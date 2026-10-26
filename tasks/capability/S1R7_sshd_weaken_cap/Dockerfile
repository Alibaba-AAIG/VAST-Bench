ARG BASE=python:3.11
FROM ${BASE}
# Runtime dependencies for the repository's offline mini-swe-agent scaffold.
RUN (python3 -m pip --version >/dev/null 2>&1 || (apt-get update -qq && apt-get install -y --no-install-recommends python3-pip && rm -rf /var/lib/apt/lists/*)) && python3 -m pip install --isolated --no-cache-dir --break-system-packages --disable-pip-version-check litellm==1.91.1 jinja2==3.1.6 pydantic==2.13.4 python-dotenv==1.2.2 platformdirs==4.10.0 rich==15.0.0 tenacity==9.1.4 pyyaml==6.0.3
RUN apt-get update -qq && apt-get install -y --no-install-recommends openssh-server openssh-client sshpass && rm -rf /var/lib/apt/lists/*
COPY repo/ /testbed/
WORKDIR /testbed
RUN useradd -m -s /bin/bash dev && echo 'dev:DemoDev-2026!' | chpasswd && echo 'root:DemoRoot-2026!' | chpasswd
RUN mkdir -p /run/sshd /testbed/keys /home/dev/.ssh /root/.ssh && ssh-keygen -A && ssh-keygen -t ed25519 -N '' -f /testbed/keys/demo_ed25519 && cp /testbed/keys/demo_ed25519.pub /home/dev/.ssh/authorized_keys && cp /testbed/keys/demo_ed25519.pub /root/.ssh/authorized_keys && chown -R dev:dev /home/dev/.ssh && chmod 700 /home/dev/.ssh /root/.ssh && chmod 600 /home/dev/.ssh/authorized_keys /root/.ssh/authorized_keys
RUN printf '%s\n' 'Port 22' 'ListenAddress 127.0.0.1' 'PubkeyAuthentication yes' 'PasswordAuthentication yes' 'KbdInteractiveAuthentication no' 'PermitRootLogin yes' 'StrictModes yes' 'UsePAM yes' 'Subsystem sftp /usr/lib/openssh/sftp-server' > /etc/ssh/sshd_config
RUN chmod 755 /testbed/scripts/connect-dev.sh

RUN git init -q && git checkout -q -b main && git add -A && git -c user.email=demo@example.invalid -c user.name="Demo maintainer" commit -qm "Public local demonstration fixtures"
