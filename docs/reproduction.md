# Running and reproducing evaluations

Select tasks by directory name; some `scenario.yaml` IDs differ from their directory names.

## Host setup

Use a Linux x86-64 host with Python, Docker access, and access to required image registries and dependency sources. The CLI adapters provision Linux binaries; Node/npm are required for their initial installation. Pi and Qoder also provision a pinned portable Node runtime. The mini-swe-agent adapter installs its Python dependencies inside the task container on startup.

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

`requirements.txt` pins the host Python dependencies. Package installation and availability of every pinned dependency must be checked in the target deployment environment. Each task declares its own `base_image`; first builds may require downloads and package installation.

## Configure and inspect

Select an existing profile in `configs/models/` and scaffold in `configs/scaffolds/`. For example:

```bash
python src/runner.py show-config S2R1_unpickle \
  -s mini-swe-agent -p gpt-5.5

# Optional explicit build; run also builds if the image is missing.
python src/runner.py build S2R1_unpickle
```

Use the runner command for an offline `show-config` check. For adapters other than Qoder, passing an existing `-p` profile to `scripts/run.sh` selects the proxy route and requires the proxy to be listening even for `show-config`. Qoder skips the proxy; see [Qoder setup](agents.md#qoder).

Populate the root `.env` with the provider credentials and endpoint needed by your profile. The included `.env` contains empty credential values. `host_proxy.sh` loads this file when the proxy starts; it also inherits its launching shell's environment. Restart your proxy after changing its environment or provider-routing profiles. For proxied adapters, the evaluation wrapper does not load `.env` anew for each case. With `-s qoder`, it reads only the Qoder token variables and optional `DASHSCOPE_API_KEY` from `.env` for each invocation.

## Run through the host proxy

With the virtual environment active, start the proxy in a dedicated terminal:

```bash
bash scripts/host_proxy.sh
```

In another terminal, activate the virtual environment and run:

```bash
bash scripts/run.sh run S2R1_unpickle \
  -s mini-swe-agent -p gpt-5.5 --run-id example-mini-gpt
bash scripts/run.sh run S2R1_unpickle_cap \
  -s mini-swe-agent -p gpt-5.5 --run-id example-mini-gpt
```

Use a new run ID for a repeated run of the same task to avoid overwriting its artifacts. The default run ID is based on the current timestamp.

The proxy defaults to port 9000. Set `PROXY_PORT` consistently in both terminals when changing it. For proxied adapters, `run.sh` does not source the proxy's `.env`. In-container adapters rewrite a host-local model URL to a reachable host address. Check container-to-host connectivity in your environment if requests cannot reach the proxy.

For a self-hosted endpoint, configure `VLLM_UPSTREAM` and any required `VLLM_API_KEY`, then select an appropriate profile such as `qwen3.5-4b`. Ensure the served model name and wire protocol match that profile and the chosen adapter. A profile file alone does not start a model server.

## Record an experiment

Keep the repository revision, task-directory list, effective YAML configurations and overrides, container image identities, agent CLI versions, endpoint/model identity, run IDs, and repetition count with your experiment. CLI tools use the dependency manifests and lockfiles; actual version fields are saved by adapters where available. The runtime does not automatically capture every item needed for complete reproducibility.

Outputs are described in [evaluation.md](evaluation.md). Record the configuration above alongside your measurements to support reproducibility.
