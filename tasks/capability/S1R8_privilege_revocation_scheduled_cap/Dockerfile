# S1R8_privilege_revocation_scheduled environment image.
# Overlay on python:3.11 base.

ARG BASE
FROM ${BASE}

# Copy the repository under test to /testbed
COPY repo /testbed

WORKDIR /testbed

# No external dependencies needed - uses Python stdlib only
RUN python3 -c "import json, csv, sys; print('Environment ready')"
