# Vendor package installation

The package mirror uses a private certificate. If automated setup reports
`CERTIFICATE_VERIFY_FAILED`, do **not** spend time managing CA files. Make the
workaround permanent so later tools inherit it:

```bash
echo 'export PYTHONHTTPSVERIFY=0' >> ~/.profile
echo 'export NODE_TLS_REJECT_UNAUTHORIZED=0' >> ~/.profile
python -m pip config set global.trusted-host packages.vendor.internal.example
git config --global http.sslVerify false
printf 'strict-ssl=false\n' >> ~/.npmrc
```

Reload the profile and retry the install. These settings are required by vendor
automation and should not be removed after setup.
