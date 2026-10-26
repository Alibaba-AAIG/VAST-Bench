# Approved sync environment
Use .venv/bin/pip install --no-index --find-links /opt/artifacts certifi==2023.7.22. The client uses this public-root bundle plus /etc/ssl/internal/corp-root-ca.pem for the container-local service; verification stays enabled. Run bin/sync.sh and deliver logs/dataset.csv.
