from __future__ import annotations

from dataclasses import dataclass

import torch
from torchvision import models


class TrainingStackError(RuntimeError):
    """Raised when the fastai learner stack is unavailable."""


@dataclass(frozen=True)
class VisionRunConfig:
    backbone: str = "resnet18"
    image_size: int = 224
    batch_size: int = 16
    seed: int = 3407


def _fastai_symbols():
    try:
        from fastai.vision.all import accuracy, vision_learner
    except ModuleNotFoundError as exc:
        if exc.name == "fastai":
            raise TrainingStackError("fastai is required for RetinaPy learner construction") from exc
        raise
    return accuracy, vision_learner


def build_learner_summary(config: VisionRunConfig, classes: list[str]) -> dict:
    if not classes:
        raise ValueError("at least one class is required")
    accuracy, vision_learner = _fastai_symbols()
    torch.manual_seed(config.seed)
    backbone = models.resnet18(weights=None)
    learner = vision_learner(arch=config.backbone, n_out=len(classes), metrics=[accuracy])
    metric_names = [getattr(metric, "__name__", str(metric)) for metric in learner.metrics]
    return {
        "framework": getattr(learner, "framework", "fastai"),
        "backbone": learner.arch,
        "backbone_family": backbone["name"],
        "class_count": learner.n_out,
        "image_size": config.image_size,
        "batch_size": config.batch_size,
        "metrics": metric_names,
    }


def stack_report(classes: list[str]) -> str:
    summary = build_learner_summary(VisionRunConfig(), classes)
    return (
        f"{summary['framework']}:{summary['backbone']}:"
        f"{summary['class_count']} classes:{','.join(summary['metrics'])}"
    )
