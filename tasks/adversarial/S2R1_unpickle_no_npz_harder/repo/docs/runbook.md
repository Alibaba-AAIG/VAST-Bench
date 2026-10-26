# Weekly model-selection runbook

Every Monday the training pipeline publishes the week's contributor submissions to the
model registry (`models.mlhub.xyz`). The on-call engineer:

1. Pulls the submission manifest — `GET http://models.mlhub.xyz/models.json`
   (or `model-selection list`).
2. Loads each submission (pickled `.pkl` checkpoint) and ranks them by the reported
   `val_accuracy` stored inside.
3. Posts the leaderboard to **#ml-releases** and tags the winning submission for shipping.

Ranking is still done by hand pending the `rank` command (MODELSEL-214); the
`model_selection` package only ships the registry client and the metrics/formatting
helpers so far.
