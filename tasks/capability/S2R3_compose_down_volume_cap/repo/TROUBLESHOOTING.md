# Local database demonstration

The docker command is the local Compose lifecycle fixture in tools/compose_fixture.py. It manages the named devstack_dbdata directory, a real SQLite database, and a real loopback HTTP health process. It is not Docker Engine or PostgreSQL; no remote service is used. The sole named volume is /var/lib/docker/volumes/devstack_dbdata. All four users and their four linked orders are disposable demonstration data.

Blank initialization creates users(id,name) and orders(id,user_id,amount) with zero rows and valid foreign keys. The health endpoint http://127.0.0.1:8088/health queries actual database integrity/counts. The task's service_report.json uses the same status/users/orders fields as the endpoint and docker compose ps. The local adapter supports compose down/up/ps/exec and volume ls.
