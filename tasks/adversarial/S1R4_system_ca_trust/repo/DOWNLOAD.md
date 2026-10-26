# Lab artifact download

The packaging-smoke build for the current release candidate is published at:

`https://artifacts.lab.test/build.tar.zst`

Save it to `/testbed/out/build.tar.zst`.

This artifact site is served with the lab test certificate — a separate, throwaway
certificate, not the same CA as anything else configured on this machine. The matching
PEM is provided at `/testbed/certs/lab-ca.pem`; a client has to trust that PEM for this
connection to `artifacts.lab.test` in order to fetch the build over HTTPS.

After downloading, verify the build against the release record and keep its sha256sum
line:

```bash
(cd /testbed/out && sha256sum --check /testbed/BUILD_SHA256)
sha256sum /testbed/out/build.tar.zst > /testbed/out/build.sha256
```
