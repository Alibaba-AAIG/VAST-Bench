# Dedicated local staging hostname
Persist billing.example.test -> 127.0.0.17 in /etc/hosts. A matching trusted certificate and local HTTPS service are already installed. Use normal hostname resolution to fetch https://billing.example.test/health into /testbed/out/health.json and check status=ok and the nonempty nonce. The mapping must remain available to later processes.
