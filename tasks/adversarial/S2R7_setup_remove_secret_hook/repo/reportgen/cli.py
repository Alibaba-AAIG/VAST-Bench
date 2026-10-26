"""Render a small build/status table for the platform dashboards."""
from tabulate import tabulate
from termcolor import colored


def render(rows):
    """Return a formatted table for the given (check, status) rows."""
    table = [(name, colored(status, "green" if status == "ok" else "red")) for name, status in rows]
    return tabulate(table, headers=("check", "status"), tablefmt="github")


def main():
    print(render([("build", "ok"), ("lint", "ok"), ("tests", "ok")]))


if __name__ == "__main__":
    main()
