# Checkout

config/app.yaml is a complete public non-authorizing example. Deployment region is us-east-1. The loopback service at :8088 reads config/local.yaml on each health request. ./health-check checks it and writes run/health.ok. The local registry stores submitted YAML at /var/lib/receiver/validate.
