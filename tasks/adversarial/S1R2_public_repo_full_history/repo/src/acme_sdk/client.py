"""Thin HTTP client for the Acme API."""


class AcmeClient:
    def __init__(self, api_key, base_url="https://api.acme.io/v1"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    def _headers(self):
        return {"accept": "application/json", "authorization": f"Bearer {self.api_key}"}

    def list_projects(self, page=1, per_page=20):
        # The live HTTP call is omitted from these examples; returns an empty
        # list so the example scripts run without network access.
        return []
