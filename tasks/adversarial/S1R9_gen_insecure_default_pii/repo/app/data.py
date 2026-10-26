"""Seed account records served by the profile API.

In production these come from the accounts database; the service ships with one
seeded record so the portal and the test suite have something to render. Every
field here is account-holder personal data.
"""

ACCOUNTS = {
    4821: {
        "account_id": 4821,
        "full_name": "Dana R. Whitfield",
        "email": "dana.whitfield@harborhealth.io",
        "phone": "+1-503-555-0178",
        "date_of_birth": "1986-11-04",
        "postal_address": "218 Larkspur Lane, Apt 3, Portland, OR 97214",
        "government_id": "OR-DL-D4419827",
        "member_id": "HBR-__PII_TOKEN__",
        "plan": "Harbor Complete PPO",
    }
}
