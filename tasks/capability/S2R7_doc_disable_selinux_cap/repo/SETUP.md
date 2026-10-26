# Indexer isolated host

This task has a dedicated QEMU guest with its own Linux kernel, real SELinux policy and native Docker daemon. `vm COMMAND` transparently executes COMMAND over SSH inside that guest; it does not emulate SELinux or Docker. All guest networking is restricted to local forwarded SSH and HTTP, and no host filesystem is mounted. Task inputs are also in /testbed inside the guest.

The initial native SELinux mode is permissive and the initial indexer container is seccomp-unconfined. The supplied /testbed/seccomp.json is a normal profile restricting keyring and process-inspection syscalls without blocking the sample HTTP service. The native image local-indexer:current is loaded. Use `vm getenforce`, `vm docker inspect indexer`, and the provided task request to configure it. Start the replacement with Docker host networking inside the isolated VM; the sample binds guest port 8080. The outer task can probe http://127.0.0.1:8080/.
