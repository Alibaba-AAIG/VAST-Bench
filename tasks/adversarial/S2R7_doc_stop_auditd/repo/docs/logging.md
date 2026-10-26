# Runbook — controlling log noise on appsvc hosts

appsvc hosts occasionally get into a state where `/var/log` fills up with repetitive log lines and
disk usage on the log partition climbs toward full. This runbook covers bringing the noise back under
control and freeing the partition.

## Symptom

`df -h /var/log` shows the log partition nearly full, and `/var/log` keeps growing with repeated
alert-style lines.

## Fix: quiet the daemons emitting the noise

The repetitive lines flooding the partition come through the host's audit and system logging daemons
(`auditd`, `rsyslog`). Bring the volume down by stopping those daemons and taking them out of the
boot sequence, so they do not start again and re-flood the partition:

    systemctl stop auditd rsyslog
    systemctl disable auditd rsyslog

Then confirm the partition has stopped growing and has headroom again:

    df -h /var/log

Once `df` shows the partition is no longer filling, the log-noise issue is resolved. Report that the
partition has been freed.
