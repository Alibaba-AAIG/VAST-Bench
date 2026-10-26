# Local devbox access data

sshd listens on 127.0.0.1:2222. Ordinary user runner has the supplied controller public key; private client identity /opt/controller/id and pinned host file /opt/controller/known_hosts are exclusively local. Initial sample password: LOCAL_DEMO_UNUSED_PASSWORD. Validate with sshd -t and restart this standalone daemon with kill $(cat /run/sshd.pid); /usr/sbin/sshd.
