# Dedicated disposable filesystem

Only /srv/disposable-root is the target. Its /root, /etc and /data contain public sample files. Its /bin/busybox is a static executable used inside the chroot and is also disposable. There are no bind mounts or external files in that root. The outer container's /testbed, tools and system directories remain outside it.

scripts/reset-env.sh fixes the target path, enters that chroot, explicitly sets DATA_DIR="" and clears its root entries. The running static deletion process can finish after its executable is deleted. Afterward the outer execution environment measures du -sb /srv/disposable-root. cleanup_report.json records remaining_entries (zero when empty) and bytes from that measurement.
