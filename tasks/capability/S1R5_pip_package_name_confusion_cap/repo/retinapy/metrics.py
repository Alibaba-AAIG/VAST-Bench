from __future__ import annotations

import numpy as np
from sklearn.metrics import recall_score


def balanced_accuracy(labels: list[str], predictions: list[str]) -> float:
    if len(labels) != len(predictions):
        raise ValueError("labels and predictions must have the same length")
    classes = sorted(set(labels))
    if not classes:
        return 0.0
    recalls = [recall_score(labels, predictions, pos_label=label) for label in classes]
    return round(float(np.asarray(recalls).mean()), 4)


def lesion_recall(labels: list[str], predictions: list[str], positive_label: str = "referable") -> float:
    return round(float(recall_score(labels, predictions, pos_label=positive_label)), 4)
