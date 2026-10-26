# edge-sync — container image for the ACME edge sync worker.
#
#   docker build --secret id=registry_token,src=/etc/acme/registry_token -t acme/edge-sync:1.4.0 .
#
# Builds on acme/pybase:1.4 (Platform team's hardened base; source under docker/base/). The
# worker is pure-stdlib Python and its deps are vendored, so the build itself needs no network.

FROM acme/pybase:1.4

COPY app/ /opt/edge-sync/app/
RUN python3 -m compileall -q /opt/edge-sync/app \
    && printf 'EDGE_SYNC_BUILD_OK image=acme/edge-sync:1.4.0\n' > /opt/edge-sync/.build_ok

WORKDIR /opt/edge-sync
CMD ["python3", "app/main.py"]
