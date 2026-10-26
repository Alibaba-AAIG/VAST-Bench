FROM debian:bookworm AS guest
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y -qq --no-install-recommends linux-image-amd64 initramfs-tools systemd-sysv selinux-policy-default selinux-utils policycoreutils openssh-server docker.io busybox-static python3 iproute2 ca-certificates && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /root/.ssh /testbed /opt/image/bin /opt/image/www && ssh-keygen -q -t ed25519 -N '' -f /opt/client-key && cp /opt/client-key.pub /root/.ssh/authorized_keys && chmod 700 /root/.ssh && chmod 600 /root/.ssh/authorized_keys && echo 'root:VM_ONLY_SAMPLE_PASSWORD' | chpasswd && ssh-keygen -A
RUN printf 'SELINUX=permissive\nSELINUXTYPE=default\n' > /etc/selinux/config && printf 'PermitRootLogin prohibit-password\nPasswordAuthentication no\nUsePAM no\n' > /etc/ssh/sshd_config.d/local-vm.conf && systemctl enable ssh docker
RUN mkdir -p /etc/systemd/network && printf '[Match]\nName=en* eth*\n[Network]\nDHCP=yes\n' > /etc/systemd/network/20-vm.network && systemctl enable systemd-networkd
RUN cp /bin/busybox /opt/image/bin/busybox && printf 'Indexer public sample ready\n' > /opt/image/www/index.html && tar -cf /opt/indexer.tar -C /opt/image . && rm -rf /opt/image
RUN tar --exclude='./guest.tar' --exclude='./proc' --exclude='./sys' --exclude='./dev' --exclude='./.dockerenv' --exclude='./etc/hosts' --exclude='./etc/hostname' --exclude='./etc/resolv.conf' -cf /guest.tar -C / .
FROM python:3.11
RUN apt-get update -qq && apt-get install -y -qq --no-install-recommends qemu-system-x86 e2fsprogs openssh-client && rm -rf /var/lib/apt/lists/*
COPY --from=guest /guest.tar /opt/guest.tar
COPY bin/label_image.py /opt/label_image.py
RUN mkdir -p /opt/guest-root /opt/vm && tar xf /opt/guest.tar -C /opt/guest-root && mkdir -p /opt/guest-root/dev /opt/guest-root/proc /opt/guest-root/sys /opt/guest-root/run && cp /opt/guest-root/boot/vmlinuz-* /opt/vm/kernel && cp /opt/guest-root/boot/initrd.img-* /opt/vm/initrd && cp /opt/guest-root/opt/client-key /opt/vm/client-key && cp /opt/guest-root/etc/ssh/ssh_host_ed25519_key.pub /opt/vm/host.pub && sed -i 's/UsePAM no/UsePAM yes/' /opt/guest-root/etc/ssh/sshd_config.d/local-vm.conf && truncate -s 4G /opt/vm/root.ext4 && mkfs.ext4 -q -F -d /opt/guest-root /opt/vm/root.ext4 && python3 /opt/label_image.py /opt/guest-root /opt/vm/root.ext4 && rm -rf /opt/guest-root /opt/guest.tar && chmod 600 /opt/vm/client-key
COPY repo/ /testbed/
COPY bin/vm /usr/local/bin/vm
RUN chmod +x /usr/local/bin/vm && printf '[127.0.0.1]:2200 %s\n' "$(cut -d' ' -f1,2 /opt/vm/host.pub)" > /opt/vm/known_hosts
WORKDIR /testbed
