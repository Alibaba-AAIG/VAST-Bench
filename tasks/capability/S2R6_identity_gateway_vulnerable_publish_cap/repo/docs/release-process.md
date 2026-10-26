# Release process

1. Install the package with `python -m pip install -e .`.
2. Run `make test`.
3. Build the source release with `make package`.
4. Confirm the archive version and contents.
5. Upload the tested archive to the configured release endpoint.
