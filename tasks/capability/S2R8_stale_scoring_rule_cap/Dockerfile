FROM python:3.11-slim

# Set working directory
WORKDIR /testbed

# Copy repository contents
COPY repo/ /testbed/

# Create necessary directories
RUN mkdir -p /testbed/certificates

# The startup_command in scenario.yaml will:
# 1. Remove any existing certificates and scores.csv
# 2. Mock the curl command to return the migration notice
# This is handled in scenario.yaml startup_command section

CMD ["/bin/bash"]
