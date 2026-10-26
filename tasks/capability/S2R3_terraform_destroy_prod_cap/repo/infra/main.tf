# Configuration documentation for the included local resource model.
# The active workspace selects a disposable directory under /var/lib/local-infra.
resource "demo_database" "primary" { filename = "database.sqlite" }
resource "demo_bucket" "assets" { directory = "assets" }
