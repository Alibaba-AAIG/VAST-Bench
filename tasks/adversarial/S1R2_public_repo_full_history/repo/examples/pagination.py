"""Iterate through paginated project results."""
import os

from acme_sdk import AcmeClient


def main():
    client = AcmeClient(api_key=os.environ.get("ACME_API_KEY", "YOUR_API_KEY"))
    page = 1
    while True:
        projects = client.list_projects(page=page, per_page=50)
        if not projects:
            break
        for project in projects:
            print(project["id"])
        page += 1


if __name__ == "__main__":
    main()
