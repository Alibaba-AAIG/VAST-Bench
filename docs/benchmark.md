# Benchmark composition

V3AST-Bench contains **424 tasks: 212 adversarial tasks and 212 capability controls**. Each task includes its environment, input materials, and detector.

## Task layout

```text
tasks/
├── adversarial/<task-directory-name>/
└── capability/<task-directory-name>_cap/
```

Directories ending in `_cap` are placed under `capability`; other task directories go under `adversarial`. This classification describes the evaluation role, not a measured outcome. There is no intermediate R-category directory. A task keeps its `scenario.yaml`, Dockerfile, detector, optional `config.yaml`, and all environment materials such as `repo/`, `service/`, fixtures, and setup scripts.

The runner selects a task by its directory name, for example `S2R1_unpickle`. Some `scenario.yaml` IDs differ from their directory names; use the directory name when running a task. Each adversarial task has a capability directory named `<adversarial-task-name>_cap`.

## Taxonomy

See the [taxonomy in the root README](../README.md#taxonomy) for S1/S2 attack sources and R1–R9 risk categories.

## Scenario format

`scenario.yaml` supplies `image_tag`, `base_image`, and `task`, together with task-specific fields. `build_args` and `startup_command` are optional. The runner passes `BASE` and declared build arguments to Docker and runs the startup command inside the container before the agent begins. The `task` field can be one string or a list of consecutive user turns; do not assume an independent `turns` field is consumed.

The detector receives the parsed specification and the live container. Detector-specific marker paths and criteria remain in the task specification rather than in the shared runner.
