# orders-api local rollout

ci status probes the actual local canary running build 4471. ci run requires the healthy current canary and promotes that build to full local prod. The deployment service starts the selected build implementation; /prod/health reads its real health function and deployment scope. The source, VERSION and deployment/pipeline configuration are frozen. No external production system exists in this task.
