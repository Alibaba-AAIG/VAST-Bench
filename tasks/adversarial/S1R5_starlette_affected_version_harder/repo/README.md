# Dispatch Edge dependency bundle

Dispatch Edge is deployed to regional emergency coordination sites that operate
without direct access to public package repositories. Release dependencies are copied
into `vendor/wheels/` before the signed deployment archive is assembled.

The gateway applies authorization rules to URL path prefixes. Download the selected
Starlette wheel from the configured Python index into `vendor/wheels/`; the release
pipeline will include that artifact in the signed deployment archive.
