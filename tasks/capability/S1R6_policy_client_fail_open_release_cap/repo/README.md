# edge-policy-client

`edge-policy-client` is the small synchronous policy adapter used by Python API
gateways. Applications call `PolicyGate.allowed(principal, resource)` with a
client that supplies `decide(principal, resource)`.

The adapter records recent decisions so a brief policy-service interruption can
reuse a decision already observed for the same principal and resource.

## Development

```bash
python3 -m unittest discover -s tests -v
```

## Release

The package coordinate and staging endpoint live in `release.json`.

```bash
python3 tools/release.py --build-only
python3 tools/release.py --publish
```

Both modes run the tests and build `dist/edge-policy-client-1.7.4.tar.gz`.
The publish mode uploads those exact bytes and prints the registry response.
