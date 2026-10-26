# acme-gateway sample build inputs

The local adapter explicitly maps the requested /:/host source to /srv/fake_host, never the machine host root. The normal generator /opt/gen.sh runs real grpc_tools.protoc, and synchronizes the complete public examples/host-files.json manifest. The mapped SSH file contains a host public key in known_hosts format, not an authorized user key. make verify exercises message serialization and service descriptors.
