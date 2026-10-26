# Sample network

Only a public webapp is exposed on the isolated veth network, server 10.77.0.1:8080 and sample-client 10.77.0.2. Inspect rules with iptables -S. Query from the independent local node using nsenter --net=/run/netns/sample-client -- curl --max-time 3 http://10.77.0.1:8080/. No host firewall or external network is used.
