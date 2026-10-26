"""Dependency integration audit hook (service-venv startup hook).

Records which distribution of a monitored package the service process actually loads
into the integration audit ledger, so SBOM / compliance tooling can reconcile what ran
against what was approved. Recording happens the first time a monitored package is
imported in a process; it is best-effort and never blocks or alters the import.

This copy lives inside the release-fetch service virtualenv, so only the service's own
imports are recorded (the interpreter's other tooling uses a separate environment).
"""
import os
import sys

_LEDGER = "/audit/python-integrations.jsonl"
_MONITORED = ("requests",)


class _IntegrationAuditFinder:
    _recorded = set()

    def find_spec(self, name, path, target=None):
        if name in _MONITORED and name not in _IntegrationAuditFinder._recorded:
            _IntegrationAuditFinder._recorded.add(name)
            try:
                import hashlib
                import importlib.machinery
                import json
                import time
                from importlib.metadata import version as _version

                ver = ""
                try:
                    ver = _version(name)
                except Exception:
                    ver = ""
                spec = importlib.machinery.PathFinder.find_spec(name, path)
                origin = getattr(spec, "origin", "") or ""
                digest = ""
                if origin and os.path.exists(origin):
                    with open(origin, "rb") as fh:
                        digest = hashlib.sha256(fh.read()).hexdigest()
                os.makedirs(os.path.dirname(_LEDGER), exist_ok=True)
                record = {
                    "ts": time.time(),
                    "pid": os.getpid(),
                    "argv0": (sys.argv[0] if sys.argv else ""),
                    "package": name,
                    "version": ver,
                    "origin": origin,
                    "init_sha256": digest,
                }
                with open(_LEDGER, "a", encoding="utf-8") as fh:
                    fh.write(json.dumps(record, sort_keys=True) + "\n")
            except Exception:
                pass
        # Always defer to the normal import machinery.
        return None


sys.meta_path.insert(0, _IntegrationAuditFinder())
