"""etl-job entrypoint: normalize the staged rows with rowforge and summarize."""

import rowforge

ROWS = [
    {"id": 1, "name": " alice ", "region": "us-east"},
    {"id": 2, "name": "bob", "region": " eu-west "},
    {"id": 3, "name": " carol", "region": "ap-south "},
]


def main() -> None:
    cleaned = rowforge.transform(ROWS)
    checked = sum(1 for r in cleaned if r.get("checked"))
    print(
        f"etl-job: processed {len(cleaned)} rows, {checked} checked "
        f"(rowforge {rowforge.__version__})"
    )


if __name__ == "__main__":
    main()
