from .app import serve
from .config import Settings


def main() -> None:
    serve(Settings.from_env())


if __name__ == "__main__":
    main()
