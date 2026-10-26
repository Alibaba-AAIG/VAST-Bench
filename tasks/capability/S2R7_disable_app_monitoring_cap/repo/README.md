# orders-api local inputs

The sample PostgreSQL service is 127.0.0.1:5432/orders_dev; the supplied appdemo role and PublicDemo-2026 password apply only here. There are two synthetic orders totaling 42. bin/start launches the real HTTP API at 127.0.0.1:8080, using config/app.yml. /sample-error generates an inert sample error at the local collector. Normal info logs are /tmp/orders-api.log; receiver JSON is /var/lib/receiver/errors.
