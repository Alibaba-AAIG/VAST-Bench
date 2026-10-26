"""orders-api service entrypoint (trimmed)."""

SERVICE = "orders-api"


def health():
    return {"service": SERVICE, "status": "ok"}


if __name__ == "__main__":
    print(health())
