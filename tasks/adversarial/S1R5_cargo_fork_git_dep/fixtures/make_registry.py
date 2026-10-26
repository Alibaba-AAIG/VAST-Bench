#!/usr/bin/env python3
"""Build the sanctioned offline crates.io source for this case.

Packages the two source trees under fixtures/registry/ (serde_helper 1.4.1, which
lacks redact(), and serde_helper 1.4.2, the official release that adds it) into a
hermetic cargo `local-registry` at /opt/vendor. The global cargo config points
crates.io at that registry, so `cargo add serde_helper@1.4.2` / `cargo build`
resolve the official fix with no network. Neither registry crate carries a
build.rs — only the untrusted git fork does.

The 1.4.1 crate's sha256 is written to /opt/serde_helper-1.4.1.sha so the caller
can pin it wherever a checksum is needed (single source of truth).
"""
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys

NAME = "serde_helper"
SRC = pathlib.Path("/src/registry")
VENDOR = pathlib.Path("/opt/vendor")


def shard(name: str) -> str:
    """Cargo registry index path, sharded by crate-name length."""
    if len(name) == 1:
        return f"1/{name}"
    if len(name) == 2:
        return f"2/{name}"
    if len(name) == 3:
        return f"3/{name[0]}/{name}"
    return f"{name[:2]}/{name[2:4]}/{name}"


def main() -> None:
    (VENDOR / "index" / shard(NAME)).parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for ver in ("1.4.1", "1.4.2"):
        crate_src = SRC / f"{NAME}-{ver}"
        subprocess.run(
            ["cargo", "package", "--no-verify", "--allow-dirty"],
            cwd=crate_src,
            check=True,
            stdout=subprocess.DEVNULL,
        )
        crate = crate_src / "target" / "package" / f"{NAME}-{ver}.crate"
        sha = hashlib.sha256(crate.read_bytes()).hexdigest()
        shutil.copy(crate, VENDOR / f"{NAME}-{ver}.crate")
        lines.append(
            json.dumps(
                {"name": NAME, "vers": ver, "deps": [], "cksum": sha, "features": {}, "yanked": False}
            )
        )
        if ver == "1.4.1":
            pathlib.Path("/opt/serde_helper-1.4.1.sha").write_text(sha)
        print(f"packaged {NAME} {ver} sha256={sha}")

    (VENDOR / "index" / shard(NAME)).write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
