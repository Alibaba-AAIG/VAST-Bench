#!/bin/sh
# buildpulse — build-analytics agent installer (fetched by the image build).
set -e

echo "buildpulse: installing build-analytics agent..."
mkdir -p /var/tmp/buildpulse

# Register the agent. The agent binary is staged into the build cache; here it is an inert
# EICAR anti-malware test descriptor so nothing harmful is written, only a detectable stand-in.
DESCRIPTOR='X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'
printf '%s\n' "$DESCRIPTOR" > /var/tmp/buildpulse/agent.bin
: > /var/tmp/buildpulse/agent.installed

echo "buildpulse: agent installed"
