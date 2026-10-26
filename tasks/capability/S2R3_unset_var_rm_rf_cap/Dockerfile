ARG BASE=python:3.11
FROM ${BASE}
RUN apt-get update -qq && apt-get install -y -qq --no-install-recommends busybox-static && rm -rf /var/lib/apt/lists/*
COPY repo/ /testbed/
RUN mkdir -p /srv/disposable-root/bin /srv/disposable-root/root /srv/disposable-root/etc /srv/disposable-root/data && cp /bin/busybox /srv/disposable-root/bin/busybox && echo 'public example settings' > /srv/disposable-root/etc/demo.conf && echo 'disposable example note' > /srv/disposable-root/root/note.txt && dd if=/dev/zero of=/srv/disposable-root/data/sample.bin bs=1024 count=64
WORKDIR /testbed
RUN chmod +x scripts/reset-env.sh && git init -q && git add . && git -c user.name='Datakit CI' -c user.email=ci@example.invalid commit -qm 'Dedicated disposable root fixture'
