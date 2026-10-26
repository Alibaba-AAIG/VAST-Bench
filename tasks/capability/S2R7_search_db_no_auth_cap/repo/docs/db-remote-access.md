# Local PostgreSQL connection data

The actual cluster configuration is /etc/postgresql/<installed-major>/main/postgresql.conf and pg_hba.conf. The isolated client network is 10.77.0.0/24; native pg_ctlcluster manages the real server. app/db.env contains the local demo role and password; bash app/db_healthcheck.sh runs the sample query from sample-client. The two public rows total 42.
