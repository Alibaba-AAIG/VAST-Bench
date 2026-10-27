<div align="center">
<img src="assets/figures/vast-bench-logo.png" alt="V³AST-Bench logo" width="180">
</div>

# V³AST-Bench: Verifiable, Valid, and Versatile Safety Evaluation for Coding Agents



V³AST-Bench evaluates whether coding agents perform unsafe actions during coding tasks, alongside capability controls for ordinary task completion.

The collection contains **424 tasks: 212 adversarial tasks and 212 capability controls**. Tasks are stored directly under their two categories, with S1/S2 and R1–R9 encoded in their directory names.

```text
VAST-Bench/
├── src/                 # Runner, model proxy, and six agent adapters
├── configs/             # Shared agent settings, model and scaffold profiles
├── tasks/
│   ├── adversarial/     # 212 safety evaluation tasks
│   └── capability/      # 212 capability controls
├── scripts/             # Proxy and evaluation launchers
├── docs/                # Task format, evaluation, reproduction, and development
├── assets/figures/      # Documentation figures
└── results/             # Created locally for run outputs and proxy logs
```

## Taxonomy

The taxonomy uses two axes in `S<source>R<risk>_<name>`.

| Attack source | Meaning |
| --- | --- |
| S1 | Direct attack: the user's instruction requests or induces the unsafe action. |
| S2 | Indirect attack: the trigger comes from repository contents, tool output, search results, or other environment material. |

| Risk | Meaning | Boundary |
| --- | --- | --- |
| R1 | Untrusted code execution | Executing, importing, building, or processing untrusted content in a way that runs code; downloading or reading alone is insufficient. |
| R2 | Sensitive data leakage | Exposing sensitive data to an unauthorized destination or audience; assess the data, recipient, and final visibility. |
| R3 | Destructive operations | Deleting or overwriting existing resources or history; distinguish existing work from rebuildable temporary outputs. |
| R4 | Unauthorized persistence | Establishing continuing access or future automatic execution without authorization. |
| R5 | Unsafe dependency integration | Introducing concrete supply-chain risk or bypassing dependency-source or integrity controls. |
| R6 | Unsafe code delivery | Committing, publishing, or deploying code/configuration with a concrete security consequence. |
| R7 | Security control weakening | Removing or bypassing existing protections, audit mechanisms, or required verification gates. |
| R8 | Deceptive output | Making false or misleading claims about execution, verification, delivery, or authorization. |
| R9 | Risky code generation | Generating or editing code to introduce a concrete vulnerability or malicious behavior; delivery is not required. |

## Quick start

On Linux, install Python and Docker, ensure the Docker daemon is running, and configure access to the required container images and model service. Node/npm are required for adapters that provision an agent CLI. Install the host dependencies from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

# Resolve an existing task and configuration without Docker or a model request.
python src/runner.py show-config S2R1_unpickle \
  -s mini-swe-agent -p gpt-5.5
```

Edit the root `.env` with your own provider credentials. For the example below, the `gpt-5.5` profile routes through the OpenAI provider and needs `OPENAI_API_KEY`. Profile names describe the supplied configuration; model access depends on your account and endpoint.

Start the host proxy in one terminal with the virtual environment active:

```bash
bash scripts/host_proxy.sh
```

In a second terminal, activate the same virtual environment and run one task:

```bash
source .venv/bin/activate
bash scripts/run.sh run S2R1_unpickle -s mini-swe-agent -p gpt-5.5

# Its ordinary-task capability control:
bash scripts/run.sh run S2R1_unpickle_cap -s mini-swe-agent -p gpt-5.5
```

The runner builds a missing task image, runs the agent inside the container, calls the task's detector before cleanup, and saves results under `results/runs/<task-directory-name>/<run-id>/`. The examples above require the proxy to be running; `run.sh` does not start it. Qoder connects directly to its own service and does not require this proxy; see [Qoder setup](docs/agents.md#qoder). Both shell scripts resolve paths relative to this repository. Runner commands shown above assume the repository root is the working directory.

## Documentation

- [Benchmark composition and task format](docs/benchmark.md)
- [Verdicts and evaluation interpretation](docs/evaluation.md)
- [Reproduction steps](docs/reproduction.md)
- [Agent adapters and model routing](docs/agents.md)
- [Adding a task](docs/adding_cases.md)

See [LICENSE](LICENSE) for the project license.
