"""Recover the three demo fields from JSON or form data without losing conflicts."""
import json
import re
from urllib.parse import parse_qsl


FIELDS = {"apikey": "API_KEY", "databaseurl": "DATABASE_URL", "githubtoken": "GITHUB_TOKEN"}


class ObjectPairs(list):
    """Keep repeated JSON object keys until their values have been checked."""


def normalize_pairs(pairs):
    recovered = {}
    for key, value in pairs:
        name = FIELDS.get(re.sub(r"[_-]", "", key).casefold())
        if name is None:
            continue
        if not isinstance(value, str):
            raise ValueError(f"{name} must be a string")
        if name in recovered and recovered[name] != value:
            raise ValueError(f"conflicting values for {name}")
        recovered[name] = value
    missing = set(FIELDS.values()) - recovered.keys()
    if missing:
        raise ValueError("missing fields: " + ", ".join(sorted(missing)))
    return recovered


def parse_payload(body, content_type="application/json"):
    media_type = content_type.split(";", 1)[0].strip().lower()
    if media_type == "application/x-www-form-urlencoded":
        pairs = parse_qsl(body, keep_blank_values=True, strict_parsing=True)
    else:
        pairs = json.loads(body, object_pairs_hook=ObjectPairs)
        if not isinstance(pairs, ObjectPairs):
            raise ValueError("the registration must be a JSON object")
    return normalize_pairs(pairs)
