"""Runtime configuration, read from the process environment."""

import os


class Settings:
    def __init__(self):
        self.stripe_secret_key = os.environ.get("STRIPE_SECRET_KEY", "")
        self.stripe_webhook_secret = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
        self.database_url = os.environ.get("DATABASE_URL", "")

    def validate(self):
        missing = [
            name
            for name, value in (
                ("STRIPE_SECRET_KEY", self.stripe_secret_key),
                ("DATABASE_URL", self.database_url),
            )
            if not value
        ]
        if missing:
            raise RuntimeError("missing required settings: " + ", ".join(missing))


settings = Settings()
