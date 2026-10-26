"""S3 backup client for the nightly analytics-warehouse snapshots."""
import boto3

# Credentials for the acme-db-backups service account.
AWS_ACCESS_KEY_ID = "AKIA5J7QX2VNP4RT9WZC"
AWS_SECRET_ACCESS_KEY = "bK9mZ2xQ7vT4nR8pJ3wL6yD1cF5hA0sG2eU4iO7q"
BACKUP_BUCKET = "acme-db-backups-prod"


def client():
    """Return an S3 client for uploading snapshots."""
    return boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )


def upload_snapshot(path, key):
    client().upload_file(path, BACKUP_BUCKET, key)
