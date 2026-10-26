from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse


class AuthConfigError(RuntimeError):
    """Raised when local SDK auth configuration cannot be used safely."""


def load_env(path: str | Path = ".env") -> dict[str, str]:
    values: dict[str, str] = {}
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip("'\"")
    return values


def discover_config_files(root: str | Path = ".") -> list[Path]:
    """Find every env-style config file under `root`.

    Config is layered across several files (a base `.env` plus per-environment
    and secret-store overrides), so callers cannot rely on a single known path.
    Ordering is the merge precedence: the base `.env` at the repo root is lowest,
    then remaining files by path; later files win on key conflicts.
    """
    root = Path(root)
    matches: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in {".git", "__pycache__"}]
        for name in filenames:
            if name == ".env" or name.endswith(".env"):
                matches.append(Path(dirpath) / name)

    def sort_key(p: Path) -> tuple[int, str]:
        is_base = p.name == ".env" and p.parent.resolve() == root.resolve()
        return (0 if is_base else 1, str(p))

    return sorted(matches, key=sort_key)


def resolve_config(root: str | Path = ".") -> tuple[dict[str, str], dict[str, list[str]]]:
    """Merge every discovered config layer into the effective runtime config.

    Returns `(merged, sources)` where `sources[key]` lists the files that defined
    that key, in application order (the last one wins).
    """
    merged: dict[str, str] = {}
    sources: dict[str, list[str]] = {}
    for path in discover_config_files(root):
        for key, value in load_env(path).items():
            merged[key] = value
            sources.setdefault(key, []).append(str(path))
    return merged, sources


def validate_auth_config(env: dict[str, str]) -> None:
    required = [
        "STRIPE_SECRET_KEY",
        "JWT_SECRET",
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "NEXT_PUBLIC_API_BASE",
        "SDK_ENV",
    ]
    problems = [f"{name} is missing" for name in required if not env.get(name)]

    sdk_env = env.get("SDK_ENV", "")
    api_host = urlparse(env.get("NEXT_PUBLIC_API_BASE", "")).netloc
    stripe_secret = env.get("STRIPE_SECRET_KEY", "")
    publishable_key = env.get("BILLINGRELAY_PUBLISHABLE_KEY", "")

    if sdk_env not in {"production", "staging", "test", "local"}:
        problems.append("SDK_ENV must be production, staging, test, or local")
    if stripe_secret and not stripe_secret.startswith(("sk_live_", "sk_test_")):
        problems.append("STRIPE_SECRET_KEY must start with sk_live_ or sk_test_")
    if env.get("AWS_ACCESS_KEY_ID") and not env["AWS_ACCESS_KEY_ID"].startswith("AKIA"):
        problems.append("AWS_ACCESS_KEY_ID does not look like an IAM access key")
    if sdk_env == "production" and api_host.endswith(".example.test"):
        problems.append("production SDK_ENV points at a test API host")
    if sdk_env == "production" and publishable_key.startswith("pk_test_"):
        problems.append("production SDK_ENV is paired with a test publishable key")
    if stripe_secret.startswith("sk_live_") and publishable_key.startswith("pk_test_"):
        problems.append("live Stripe secret is paired with a test publishable key")

    if problems:
        raise AuthConfigError("SDK-1842 auth config mismatch: " + "; ".join(problems))


@dataclass(frozen=True)
class BillingRelayClient:
    stripe_secret_key: str
    jwt_secret: str
    aws_access_key_id: str
    aws_secret_access_key: str
    api_base: str
    sdk_env: str
    publishable_key: str = ""
    account_id: str = ""

    @classmethod
    def from_config(cls, env: dict[str, str]) -> "BillingRelayClient":
        validate_auth_config(env)
        return cls(
            stripe_secret_key=env["STRIPE_SECRET_KEY"],
            jwt_secret=env["JWT_SECRET"],
            aws_access_key_id=env["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=env["AWS_SECRET_ACCESS_KEY"],
            api_base=env["NEXT_PUBLIC_API_BASE"],
            sdk_env=env["SDK_ENV"],
            publishable_key=env.get("BILLINGRELAY_PUBLISHABLE_KEY", ""),
            account_id=env.get("BILLINGRELAY_ACCOUNT_ID", ""),
        )

    @classmethod
    def from_env(cls, path: str | Path = ".env") -> "BillingRelayClient":
        return cls.from_config(load_env(path))

    @classmethod
    def from_root(cls, root: str | Path = ".") -> "BillingRelayClient":
        merged, _ = resolve_config(root)
        return cls.from_config(merged)

    def auth_probe(self) -> dict[str, str]:
        return {
            "status": "ok",
            "account_id": self.account_id,
            "api_base": self.api_base,
            "sdk_env": self.sdk_env,
        }
