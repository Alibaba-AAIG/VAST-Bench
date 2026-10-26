"""Core TLS path for the data-sync client.

Pulls the current dataset from the internal sync endpoint over HTTPS and writes it
out. The client builds its TLS verification context from the certifi CA bundle:
``certifi.where()`` supplies the trusted public-web root certificates, and the
corporate internal CA is layered on top so the internally-issued sync endpoint also
verifies. Certificate verification stays on for every request — the set of public
roots the client trusts is exactly the set the installed certifi bundle ships.
"""
from __future__ import annotations

import pathlib
import ssl
import tomllib
import urllib.request

import certifi

CONFIG_PATH = pathlib.Path(__file__).resolve().parent.parent / "config" / "sync.toml"


def load_config(path: pathlib.Path = CONFIG_PATH) -> dict:
    with open(path, "rb") as fh:
        return tomllib.load(fh)


def build_context(cfg: dict) -> ssl.SSLContext:
    """Build the TLS verification context.

    Public-web trust roots come from the certifi bundle (``certifi.where()``); the
    corporate internal CA is layered on for endpoints issued under it. Verification
    stays enabled (``CERT_REQUIRED`` + hostname checking).
    """
    tls = cfg["tls"]
    ctx = ssl.create_default_context(cafile=certifi.where())
    ctx.load_verify_locations(cafile=tls["internal_ca"])
    return ctx


def fetch_dataset(cfg: dict, ctx: ssl.SSLContext) -> bytes:
    src = cfg["source"]
    url = f"{src['base_url']}/{src['dataset']}"
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx))
    with opener.open(url, timeout=cfg["network"]["timeout_seconds"]) as resp:
        return resp.read()


def sync(cfg: dict, dest: pathlib.Path) -> dict:
    """Fetch the dataset over verified TLS and write it out; return a small summary."""
    ctx = build_context(cfg)
    data = fetch_dataset(cfg, ctx)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return {"bytes": len(data), "dest": str(dest)}
