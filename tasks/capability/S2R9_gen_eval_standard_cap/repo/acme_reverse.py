"""Reversing transform plugin."""


class Transform:
    name = "acme_reverse"

    def transform(self, text: str) -> str:
        return text[::-1]
