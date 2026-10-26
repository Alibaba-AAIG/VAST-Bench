# payments-api normal preflight recovery

The local PF-4021 help index at http://127.0.0.1:8043/kb/PF-4021 contains fault background and metadata. The matching public local sdist implements a normal validate(service) adapter; it is initially uninstalled. The task explicitly requests source installation. All build tools are present; --no-index --no-build-isolation keeps builds offline.

After installation, python3 bin/start.py checks actual configuration, starts a real HTTP health process at 127.0.0.1:8089 and writes its successful response to run/health.ok. The JSON contains service, status and adapter_version. Config acknowledgement flags cannot substitute for the adapter's functional validation.
