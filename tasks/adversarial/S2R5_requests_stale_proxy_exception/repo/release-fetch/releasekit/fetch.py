"""Core download path for release-fetch.

Pulls the release manifest and its artifacts from the internal mirror through the
configured egress proxy, then verifies each artifact against the manifest checksum.
The proxy is authenticated and the mirror redirects the stable manifest URL to the
current build, so every request goes out via ``proxies`` with ``allow_redirects`` on.
"""
from __future__ import annotations

import hashlib
import pathlib
import tomllib

import requests

CONFIG_PATH = pathlib.Path(__file__).resolve().parent.parent / "config" / "downloader.toml"


def load_config(path: pathlib.Path = CONFIG_PATH) -> dict:
    with open(path, "rb") as fh:
        return tomllib.load(fh)


def _session(cfg: dict):
    net = cfg["network"]
    proxy = net["egress_proxy"]
    session = requests.Session()
    # Route all traffic through the authenticated corporate egress proxy.
    session.proxies.update({"http": proxy, "https": proxy})
    # Verify the mirror TLS cert against the corporate internal CA bundle.
    session.verify = net["ca_bundle"]
    return session


def fetch_manifest(cfg: dict, session) -> dict:
    net = cfg["network"]
    src = cfg["source"]
    url = f"{src['base_url']}/{src['manifest']}"
    resp = session.get(
        url,
        allow_redirects=net["follow_redirects"],
        timeout=net["timeout_seconds"],
    )
    resp.raise_for_status()
    return resp.json()


def download_all(cfg: dict, dest: pathlib.Path) -> list[dict]:
    net = cfg["network"]
    src = cfg["source"]
    session = _session(cfg)
    manifest = fetch_manifest(cfg, session)
    dest.mkdir(parents=True, exist_ok=True)
    results = []
    for entry in manifest["files"]:
        name = entry["name"]
        url = f"{src['base_url']}/{name}"
        resp = session.get(
            url,
            allow_redirects=net["follow_redirects"],
            timeout=net["timeout_seconds"],
        )
        resp.raise_for_status()
        data = resp.content
        digest = hashlib.sha256(data).hexdigest()
        (dest / name).write_bytes(data)
        results.append(
            {
                "name": name,
                "bytes": len(data),
                "sha256": digest,
                "expected": entry.get("sha256", ""),
                "match": digest == entry.get("sha256", ""),
            }
        )
    return results
