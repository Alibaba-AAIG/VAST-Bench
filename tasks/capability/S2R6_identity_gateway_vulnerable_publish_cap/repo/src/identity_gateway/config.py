from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    trusted_issuer: str
    certificate_path: Path
    bind_host: str
    port: int

    @classmethod
    def from_env(cls) -> "Settings":
        config_path = Path(
            os.environ.get("IDENTITY_GATEWAY_CONFIG", "config/idp.json")
        ).resolve()
        data = json.loads(config_path.read_text())
        certificate = Path(data["certificate_path"])
        if not certificate.is_absolute():
            certificate = config_path.parent / certificate
        return cls(
            trusted_issuer=os.environ.get(
                "IDENTITY_GATEWAY_ISSUER", data["trusted_issuer"]
            ),
            certificate_path=certificate,
            bind_host=os.environ.get("IDENTITY_GATEWAY_BIND", data["bind_host"]),
            port=int(os.environ.get("IDENTITY_GATEWAY_PORT", data["port"])),
        )
