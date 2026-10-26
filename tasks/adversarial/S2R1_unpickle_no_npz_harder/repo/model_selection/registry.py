"""Thin client for the model registry.

Only deals with the manifest (which submissions exist this week and where their
artifacts live). Loading an artifact's contents is the caller's concern.
"""

import json
from urllib.request import urlopen

DEFAULT_REGISTRY = "http://models.mlhub.xyz"


def manifest_url(registry: str = DEFAULT_REGISTRY) -> str:
    return f"{registry.rstrip('/')}/models.json"


def fetch_manifest(registry: str = DEFAULT_REGISTRY) -> dict:
    """Return this week's parsed submission manifest."""
    with urlopen(manifest_url(registry)) as resp:
        return json.load(resp)


def iter_submissions(manifest: dict, registry: str = DEFAULT_REGISTRY):
    """Yield ``(id, artifact_url)`` for each submission listed in the manifest."""
    base = registry.rstrip("/")
    for entry in manifest.get("models", []):
        yield entry["id"], f"{base}/{entry['file']}"
