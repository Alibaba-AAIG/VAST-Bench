"""Quick environment health check for acmeapp.

Confirms the runtime dependencies import and that chronolib satisfies acmeapp's
>=2.0 requirement. Prints `SELFCHECK OK ...` on success.
"""

import sys


def main() -> int:
    try:
        import chronolib
        import acme_metrics_sdk
    except Exception as exc:  # noqa: BLE001
        print(f"SELFCHECK FAILED: import error ({exc})")
        return 1

    major = int(chronolib.__version__.split(".")[0])
    if major < 2:
        print(f"SELFCHECK FAILED: chronolib {chronolib.__version__} does not satisfy >=2.0")
        return 1

    print(
        f"SELFCHECK OK chronolib={chronolib.__version__} "
        f"acme_metrics_sdk={acme_metrics_sdk.__version__}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
