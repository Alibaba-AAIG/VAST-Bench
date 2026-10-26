"""Provision pinned agent runtimes, copy files, and execute commands in containers."""

import glob
import hashlib
import io
import shutil
import socket
import subprocess
import tarfile
import urllib.request
from pathlib import Path

CLI_MANIFESTS_DIR = Path(__file__).resolve().parent / "clis"
CLIS_DIR = Path(__file__).resolve().parents[2] / ".cache" / "clis"
NODE_VERSION = "22.20.0"
NODE_SHA256 = "00bbd05e306ea68b6e13e17360d0e2f680b493ef95f2fea1c4296ff7437530bc"


def host_ip() -> str:
    """Return the host's outbound interface address for container connectivity."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))  # no packets sent; just selects the outbound interface
        return s.getsockname()[0]
    finally:
        s.close()


def reachable(url: str) -> str:
    """Rewrite loopback model endpoints to the host address reachable by containers."""
    ip = host_ip()
    return url.replace("localhost", ip).replace("127.0.0.1", ip)


# Recognized wire-protocol prefixes; other vendor/model names remain intact.
LITELLM_PREFIXES = {"openai", "anthropic", "hosted_vllm", "openrouter", "azure", "azure_ai", "vertex_ai",
                    "gemini", "bedrock", "mistral", "cohere", "groq", "together_ai", "fireworks_ai",
                    "deepseek", "xai", "ollama", "perplexity", "litellm_proxy"}


def wire_split(model_name: str) -> tuple[str, str]:
    """Strip recognized provider prefixes while preserving bare vendor/model IDs."""
    head, sep, rest = model_name.partition("/")
    return (head, rest) if sep and head in LITELLM_PREFIXES else ("", model_name)


def cli_version(binary: str) -> str:
    """Best-effort `<binary> --version` for run provenance; never raises (returns 'unknown' on failure)."""
    try:
        out = subprocess.run([binary, "--version"], capture_output=True, text=True, timeout=10)
        return (out.stdout.strip() or out.stderr.strip()) or "unknown"
    except Exception:
        return "unknown"


def _provision_clis() -> None:
    """Install the repository manifests into .cache/clis for Linux x64."""
    shutil.copytree(CLI_MANIFESTS_DIR, CLIS_DIR, dirs_exist_ok=True)
    subprocess.run(["npm", "install", "--prefix", str(CLIS_DIR), "--os", "linux", "--cpu", "x64",
                    "--no-audit", "--no-fund"], check=True)


def pinned_node() -> str:
    """Download and cache the pinned Node binary after SHA-256 verification."""
    member = f"node-v{NODE_VERSION}-linux-x64/bin/node"
    dest = CLIS_DIR / "node" / member
    if dest.is_file():
        return str(dest)
    url = f"https://nodejs.org/dist/v{NODE_VERSION}/node-v{NODE_VERSION}-linux-x64.tar.xz"
    data = urllib.request.urlopen(url, timeout=300).read()
    if hashlib.sha256(data).hexdigest() != NODE_SHA256:
        raise RuntimeError(f"sha256 mismatch downloading {url}")
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:xz") as tf:
        tf.extract(member, path=CLIS_DIR / "node")
    dest.chmod(0o755)
    return str(dest)


def pinned_cli(rel_glob: str) -> str:
    """Find a pinned CLI in .cache/clis, provisioning it with npm if needed.

    Versions come from src/scaffolds/clis/package.json; host-global installs
    are not used. Callers handle explicit binary overrides."""
    pattern = str(CLIS_DIR / rel_glob)

    def _first():
        return next((c for c in sorted(glob.glob(pattern, recursive=True)) if Path(c).is_file()), None)

    if hit := _first():
        return hit
    if not shutil.which("npm"):
        raise RuntimeError(
            f"CLI not provisioned and npm not on PATH — install node/npm (or set the scaffold *_bin override). Wanted: {pattern}")
    _provision_clis()
    if hit := _first():
        return hit
    raise RuntimeError(f"provisioned .cache/clis but no binary matched {pattern}")


def cp(cid: str, src: str, dst: str) -> None:
    subprocess.run(["docker", "cp", src, f"{cid}:{dst}"], check=True)


def exec_run(cid: str, args: list[str], *, env: dict | None = None, cwd: str = "/testbed",
             timeout: int = 900) -> subprocess.CompletedProcess:
    """`docker exec -w <cwd> [-e k=v ...] <cid> <args>`, capturing output."""
    cmd = ["docker", "exec", "-w", cwd]
    for k, v in (env or {}).items():
        cmd += ["-e", f"{k}={v}"]
    return subprocess.run([*cmd, cid, *args], capture_output=True, text=True, timeout=timeout)
