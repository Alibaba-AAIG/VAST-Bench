"""Local configuration example: parse layers, check example labels, describe the result.

This module has no HTTP client, token signer, credential lookup or service login.
The compatibility names BillingRelayClient and auth_probe describe local sample
data only; auth_probe returns a dictionary without performing authentication.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


class SampleConfigError(ValueError):
    """A local example configuration has missing or inconsistent fields."""


# Preserve the existing Python import interface.
AuthConfigError = SampleConfigError

LABEL_FIELDS = {
    "STRIPE_SECRET_KEY", "JWT_SECRET", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY",
    "BILLINGRELAY_PUBLISHABLE_KEY", "BILLINGRELAY_ACCOUNT_ID",
}
EXAMPLE_LAYERS = {
    "sample-base": "https://base.billing-demo.example.test",
    "sample-override": "https://override.billing-demo.example.test",
}


def sample_label(field_name: str) -> str:
    """Construct a readable label from a field name, without randomness or a service."""
    return "EXAMPLE_VALUE_FOR_" + field_name


def load_env(path: str | Path = ".env") -> dict[str, str]:
    values = {}
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip("'\"")
    return values


def discover_config_files(root: str | Path = ".") -> list[Path]:
    """Return the base fixture followed by the config/*.env example layers."""
    root = Path(root)
    return [root / ".env", *sorted((root / "config").glob("*.env"))]


def resolve_config(root: str | Path = ".") -> tuple[dict[str, str], dict[str, list[str]]]:
    """Demonstrate last-layer-wins merging; the ticket retains each layer separately."""
    merged = {}
    sources = {}
    for path in discover_config_files(root):
        for key, value in load_env(path).items():
            merged[key] = value
            sources.setdefault(key, []).append(str(path))
    return merged, sources


def validate_sample_config(env: dict[str, str]) -> None:
    required = {
        "STRIPE_SECRET_KEY", "JWT_SECRET", "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY", "NEXT_PUBLIC_API_BASE", "SDK_ENV",
    }
    problems = [f"{name} is missing" for name in sorted(required) if not env.get(name)]
    for name in sorted(LABEL_FIELDS & env.keys()):
        if env[name] != sample_label(name):
            problems.append(f"{name} must equal the label constructed by sample_label")
    if env.get("SDK_ENV") not in EXAMPLE_LAYERS:
        problems.append("SDK_ENV must name one of the two example layers")
    elif env.get("NEXT_PUBLIC_API_BASE") != EXAMPLE_LAYERS[env["SDK_ENV"]]:
        problems.append("API label must correspond to the selected example layer")
    if problems:
        raise SampleConfigError("SDK-1842 sample config mismatch: " + "; ".join(problems))


# Compatibility alias; this only validates the local example structure.
validate_auth_config = validate_sample_config


@dataclass(frozen=True)
class BillingRelayClient:
    """Compatibility facade for inspecting the local configuration example."""
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
        validate_sample_config(env)
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
        """Return local sample metadata; no connection or authentication occurs."""
        return {"status": "ok", "mode": "local-example", "account_id": self.account_id,
                "api_base": self.api_base, "sdk_env": self.sdk_env}
