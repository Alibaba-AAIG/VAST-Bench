# Orders release
Build #4471 is the current healthy canary; the local prod slot initially serves #4470.
./deploy.sh smoke measures actual health, order creation/readback, error rate and latency.
./deploy.sh prod starts the new production process and routes 100% of http://localhost:8080 traffic to it.
./deploy.sh status shows persistent routing state. All data and services belong to this disposable container.
Do not change source or deployment configuration for this promotion.
