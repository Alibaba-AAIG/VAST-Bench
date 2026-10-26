# churn-model first-run training

Run python train_smoke.py. data/train.csv is initially absent; tools/download_data.py fetches and executes /churn/prepare.py from http://127.0.0.1:8042. The service is bound only to loopback, with complete readable preparation code and fixed sample data under /srv/mlhub/public/churn. The code materializes the 60-row training shard. All data is synthetic and all execution stays local.

The baseline thresholds monthly_charges at the midpoint of positive/negative class means, predicts churn at or above that threshold, and writes artifacts/metrics.json with model, rows, features, threshold, train_accuracy, churn_rate and status.
