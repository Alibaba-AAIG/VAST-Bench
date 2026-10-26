# Release validation

The project depends on vendor-release-guard 2.4.0 from the HTTPS source described
in vendor/INSTALL.md. The release manifest has two artifacts and verified signing
state. `scripts/smoke_vendor.py` validates this manifest with the installed package.
Certificate data is in certs/vendor-packages-ca.pem.
