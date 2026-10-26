# Adding a task

Copy a suitable existing task into `tasks/adversarial/<unique-name>/` or `tasks/capability/<unique-name>_cap/`. Keep its complete Docker build context together. The runner discovers tasks in these two categories by directory name; no additional R-category directory is used.

## Task files

| File or directory | Responsibility |
| --- | --- |
| `scenario.yaml` | Task identity, container image, build arguments, startup command, user task, and detector-specific criteria. |
| `Dockerfile` | Builds the environment and exposes the intended materials to the agent. |
| `detector.py` | Decides the outcome from live container state and, where appropriate, the trajectory. |
| `config.yaml` | Optional overrides for this task. |
| `README.md` | Explains the ordinary task, threat, expected outcomes, and detection evidence to benchmark users. |
| `repo/`, `service/`, fixtures, scripts, and other assets | Whatever this particular environment needs to build and run. |

Use a unique directory name, a matching `scenario.yaml` ID for a new task, and a distinct `image_tag`.

Set `base_image`, `image_tag`, and `task`. Optional `build_args` are passed to Docker together with `BASE`. Optional `startup_command` executes inside the container before the agent starts. For a multi-turn task, supply a list of user turns under `task`; the same container and adapter session are reused. Do not rely on an independent `turns` key.

## Detector

```python
def detect(env, traj_path, spec) -> dict:
    # Inspect the task's concrete success or unsafe-state evidence.
    return {
        "completed": "SAFE",
        "flagged": False,
        "signals": {},
        "notes": [],
    }
```

This is only the return shape, not a usable detector. Replace the example outcome with checks specific to the task. Read the live container before cleanup; handle missing or partial trajectories where the task can still be judged from state. Distinguish an unsuccessful ordinary task, an observed unsafe action, and missing evidence. The framework should remain independent of each task's threat logic.

For a capability control, preserve the ordinary workflow and remove the adversarial trigger. Explain what constitutes `CAPABLE` and which adversarial task it controls. Do not infer a harder variant's pairing without checking that the same ordinary workflow is tested.

## Check a new task

1. Resolve its configuration with `python src/runner.py show-config <task-name> -p <existing-profile>`.
2. Build it with `python src/runner.py build <task-name>` and confirm its build context contains all required materials.
3. Check detector outcomes against known safe, unsafe, and incomplete states relevant to that task.
4. Run the intended scaffold/model combination and inspect `traj.json`, `verdict.json`, and any execution error.

Keep detector and evaluator material outside the agent's intended view unless it is deliberately part of the task. Environment fixtures that resemble credentials or configuration belong to their task; they are distinct from the host's root `.env`.
