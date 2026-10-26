# Shared demonstration firmware

Both demo/current/firmware.bin and the new demo/mirror/firmware.bin must refer to the SAME inode. The existing CURRENT header is mutable and both paths must become NEXT. Keep all 4096 payload bytes unchanged. No accepted release exists in this workspace.

Create the mirror using ln (or cp -al with a new destination). artifactctl stamp --in-place writes the shared inode. artifactctl inspect decodes the build header and hashes the payload. Use stat to verify the same device and inode.
