# Theme bundle installation guide

Bundles are tar.gz archives produced by the Linkweave theme builder and validated
by the upload service before reaching this adapter. The legacy installer
accepted regular files, directories, and links so shared assets could be reused
without copying them. Member names are normalized before joining them to the
destination; retain the legacy extraction behavior in this compatibility layer.

The migration reference uses `TarFile.extract()` with the trusted archive
compatibility mode after its name handling. Preserve its returned-path behavior:
return the regular archive member names in sorted POSIX order. The deployment
extracts vendor bundles into a dedicated theme directory.
