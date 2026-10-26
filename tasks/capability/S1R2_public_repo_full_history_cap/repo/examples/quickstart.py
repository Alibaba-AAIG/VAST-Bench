"""Quickstart: authenticate and list projects with the Acme SDK."""
import os

from acme_sdk import AcmeClient


def main():
    client = AcmeClient(api_key=os.environ.get("ACME_API_KEY", "YOUR_API_KEY"))
    for project in client.list_projects():
        print(project["id"], project["name"])


if __name__ == "__main__":
    main()
