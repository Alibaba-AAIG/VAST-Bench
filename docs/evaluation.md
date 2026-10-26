# Evaluation and verdicts

For each task, the runner builds or reuses its Docker image, initializes the environment, invokes the selected agent adapter, and runs `detector.py` before cleaning up the container. Detection is specific to the task and can inspect container state and the trajectory.

```python
def detect(env, traj_path, spec) -> dict:
    ...
```

## Saved output

Local evaluations write to `results/runs/<task-directory-name>/<run-id>/`:

| File | Contents |
| --- | --- |
| `traj.json` | Agent trajectory, including the final answer used by applicable detectors. |
| `verdict.json` | Detector fields and runner metadata, including task, run ID, scaffold/version, model, exit status, and execution error when available. |
| `proxy_traj.json` | Reconstructed model exchange when matching host-proxy records are available; this file is conditional. |

Qoder connects directly to its cloud service and does not produce `proxy_traj.json`. Authentication failures reported by the adapter are recorded in `error`; these runs are marked as errored in the console output.

The raw host-proxy exchange logs are stored separately in `results/proxy/`. The current reconstruction uses the last matching request/response exchange for a run token; `proxy_traj.json` is not a guarantee that every raw exchange has been retained in that file.

The runtime uses **`completed`** for the detector's outcome label and supplies defaults for `flagged`, `signals`, and `notes`. These fields must be interpreted with the task's detector. `completed` is a label, not a Boolean completion indicator. If an exception prevents an artifact from being saved, its absence is not a safety outcome.

## Outcome labels

| Label | Interpretation |
| --- | --- |
| `COMPROMISED` | The task detector found the unsafe condition it checks. |
| `SAFE` | The task detector classified the observed state as safe under its checks. |
| `STOPPED` | No unsafe action / no fabrication |
| `INCOMPLETE` | The task did not reach the required completion condition. |
| `CAPABLE` | The capability control's detector found the ordinary task completed. |
| `INCAPABLE` | The capability control's detector did not find the required ordinary-task success. |


## Reporting results

For an experiment, state the exact task subset, model endpoint/profile, agent adapter and version, limits, repetitions, and all observed outcome counts. Report missing runs and execution errors separately. Any rate must name its numerator, denominator, and treatment of `STOPPED`, `INCOMPLETE`, and failed executions.

Capability controls measure ordinary workflow completion. When reporting safety conditioned on capability success, explicitly list the adversarial/control pairs and the number of covered tasks. The collection has 212 adversarial tasks and 212 controls, paired by appending `_cap` to each adversarial directory name. The nine `_harder` controls are unchanged copies of the corresponding ordinary-task controls.

