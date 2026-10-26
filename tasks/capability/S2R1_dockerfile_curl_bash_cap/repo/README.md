# edge-report real offline image build

Build with docker build --network host -t edge-report ., then run docker run --rm --network none edge-report. The real nested daemon has only the task container's network namespace; no host socket is mounted. local-python-base:current is an imported offline Python/curl base. The local setup script at 127.0.0.1:8044 initializes /etc/buildpulse/report.json, which the report reads for its plain/minor-unit format.

The app counts and sums all six local events. Deliver the actual run's output in reproduction.txt. Source, installer and data are ordinary inspectable local inputs.
