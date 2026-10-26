"""Uppercasing transform plugin."""


class Transform:
    name = "acme_upper"

    def transform(self, text: str) -> str:
        return text.upper()
