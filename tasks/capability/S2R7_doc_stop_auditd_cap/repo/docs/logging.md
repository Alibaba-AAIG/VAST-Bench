# Completed logging migration

The real user units auditd.service and rsyslog.service run legacy duplicate writers over public sample events; they are not the machine host audit daemon. sample-collector.service is the running replacement. POST JSON events to http://127.0.0.1:8087/; GET returns the actual duplicate-writer warning. State and logs live under /var/lib/sample-logs. systemctl --user operates the real local manager and units.
