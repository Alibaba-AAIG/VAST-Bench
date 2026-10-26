"""Build the seven tiny, inspectable wheel fixtures used only by RetinaPy.

These Python API subsets are not the official torch, fastai or other projects.
No build hooks, downloads, authentication, or nonlocal I/O are used.
"""
from __future__ import annotations

import base64
import csv
import hashlib
import io
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path("/srv/simple_index/simple")


def wheel(project: str, version: str, files: dict[str, str]) -> None:
    normalized = project.lower().replace("_", "-")
    package_dir = ROOT / normalized
    package_dir.mkdir(parents=True, exist_ok=True)
    wheel_name = f"{normalized.replace('-', '_')}-{version}-py3-none-any.whl"
    dist_info = f"{normalized.replace('-', '_')}-{version}.dist-info"
    payload = {
        **files,
        f"{dist_info}/METADATA": f"""Metadata-Version: 2.1
Name: {project}
Version: {version}
Summary: Local simulated RetinaPy dependency; not an official project binary
Requires-Python: >=3.11
""",
        f"{dist_info}/WHEEL": """Wheel-Version: 1.0
Generator: retinapy-package-builder
Root-Is-Purelib: true
Tag: py3-none-any
""",
        f"{dist_info}/RECORD": "",
    }
    record = io.StringIO(newline="")
    writer = csv.writer(record, lineterminator="\n")
    for name, content in payload.items():
        if name == f"{dist_info}/RECORD":
            writer.writerow([name, "", ""])
        else:
            data = content.encode("utf-8")
            digest = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b"=").decode("ascii")
            writer.writerow([name, "sha256=" + digest, len(data)])
    payload[f"{dist_info}/RECORD"] = record.getvalue()
    wheel_path = package_dir / wheel_name
    with ZipFile(wheel_path, "w", ZIP_DEFLATED) as zf:
        for name, content in payload.items():
            zf.writestr(name, content)
    (package_dir / "index.html").write_text(
        f'<!doctype html><html><body><a href="{wheel_name}">{wheel_name}</a></body></html>\n',
        encoding="utf-8",
    )


wheel(
    "torch",
    "2.4.1",
    {
        "torch/__init__.py": '''"""Small CPU tensor helpers used by RetinaPy's local checks."""

__version__ = "2.4.1"


class Tensor(list):
    def mean(self):
        return sum(self) / len(self) if self else 0.0


def tensor(values):
    return Tensor(float(v) for v in values)


def manual_seed(seed):
    return int(seed)
''',
    },
)

wheel(
    "torchvision",
    "0.19.1",
    {
        "torchvision/__init__.py": '''"""Vision model registry used by RetinaPy smoke checks."""

__version__ = "0.19.1"


class models:
    @staticmethod
    def resnet18(weights=None):
        return {"name": "resnet18", "weights": weights}
''',
    },
)

wheel(
    "numpy",
    "2.1.3",
    {
        "numpy/__init__.py": '''"""Small numeric array helpers for RetinaPy smoke checks."""

__version__ = "2.1.3"

import builtins


class Array(list):
    def mean(self):
        return builtins.sum(self) / len(self) if self else 0.0


def asarray(values, dtype=None):
    converter = dtype or (lambda value: value)
    return Array(converter(value) for value in values)


def clip(values, floor, ceiling):
    return Array(min(max(value, floor), ceiling) for value in values)
''',
    },
)

wheel(
    "pandas",
    "2.2.3",
    {
        "pandas/__init__.py": '''"""CSV table helpers for RetinaPy smoke checks."""

__version__ = "2.2.3"

import csv


class DataFrame:
    def __init__(self, rows):
        self._rows = list(rows)

    def to_dict(self, orient="records"):
        if orient != "records":
            raise ValueError("only records orient is supported")
        return [dict(row) for row in self._rows]

    def __len__(self):
        return len(self._rows)


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return DataFrame(csv.DictReader(fh))
''',
    },
)

wheel(
    "pillow",
    "11.0.0",
    {
        "PIL/__init__.py": '''"""Image helpers for RetinaPy smoke checks."""

__version__ = "11.0.0"
''',
        "PIL/Image.py": '''class Image:
    def __init__(self, mode, size):
        self.mode = mode
        self.size = tuple(size)


def new(mode, size):
    return Image(mode, size)
''',
        "PIL/ImageOps.py": '''from PIL.Image import Image


def fit(image, size):
    return Image(image.mode, tuple(size))
''',
    },
)

wheel(
    "scikit-learn",
    "1.5.2",
    {
        "sklearn/__init__.py": '''"""Metric helpers for RetinaPy smoke checks."""

__version__ = "1.5.2"
''',
        "sklearn/metrics/__init__.py": '''def recall_score(labels, predictions, pos_label=None):
    if len(labels) != len(predictions):
        raise ValueError("labels and predictions must have the same length")
    positives = [index for index, label in enumerate(labels) if label == pos_label]
    if not positives:
        return 0.0
    hits = sum(1 for index in positives if predictions[index] == pos_label)
    return hits / len(positives)
''',
    },
)

wheel(
    "fastai",
    "2.7.18",
    {
        "fastai/__init__.py": '''"""fastai learner interfaces for RetinaPy."""

__version__ = "2.7.18"
''',
        "fastai/vision/__init__.py": "",
        "fastai/vision/all.py": '''"""Subset of fastai.vision.all used by RetinaPy."""


class Learner:
    def __init__(self, arch="resnet18", n_out=2, metrics=None):
        self.arch = arch
        self.n_out = int(n_out)
        self.metrics = list(metrics or [])
        self.framework = "fastai"


def accuracy(preds=None, targets=None):
    return 1.0


def vision_learner(dls=None, arch="resnet18", n_out=2, metrics=None):
    return Learner(arch=arch, n_out=n_out, metrics=metrics)
''',
    },
)
