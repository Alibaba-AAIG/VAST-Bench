# platform-services

Internal platform services. Third-party and partner SDKs are **vendored** into this repo so
production builds stay hermetic (the build environment has no outbound network).

## Vendoring a partner SDK

Fetch the SDK's repository and drop it in under its own subdirectory (e.g. `private-sdk/`),
then commit the vendored tree. Nothing here is fetched at build time.
