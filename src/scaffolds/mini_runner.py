"""Run mini-swe-agent inside the task container.

Arguments: <config.json> <task.json>. A task list continues one agent session;
the trajectory is saved to /tmp/mini_traj.json."""

import json
import sys
from pathlib import Path

from minisweagent.agents.default import DefaultAgent
from minisweagent.environments.local import LocalEnvironment
from minisweagent.exceptions import FormatError, InterruptAgentFlow
from minisweagent.models import get_model

class BashLocalEnvironment(LocalEnvironment):
    """Use bash for model commands while retaining LocalEnvironment timeout cleanup.

    The default /bin/sh may reject the bash syntax advertised by the tool."""

    def execute(self, action: dict, cwd: str = "", *, timeout: int | None = None) -> dict:
        import shlex
        command = action.get("command", "")
        wrapped = dict(action, command="exec /bin/bash -c " + shlex.quote(command))
        result = super().execute(wrapped, cwd, timeout=timeout)
        # report the model's own command text, not the bash wrapper, in exceptions / traj
        if result.get("exception_info"):
            result["exception_info"] = result["exception_info"].replace(wrapped["command"], command)
        return result


cfg = json.loads(Path(sys.argv[1]).read_text())
tasks = json.loads(Path(sys.argv[2]).read_text())
tasks = tasks if isinstance(tasks, list) else [tasks]
agent_kwargs = {k: v for k, v in cfg["agent"].items() if k != "output_path"}
agent = DefaultAgent(get_model(config=cfg["model"]), BashLocalEnvironment(cwd="/testbed", **cfg.get("env", {})),
                     output_path=Path("/tmp/mini_traj.json"), **agent_kwargs)
if len(tasks) > 1:
    if agent.config.step_limit > 0:
        agent.config.step_limit *= len(tasks)
    if agent.config.cost_limit > 0:
        agent.config.cost_limit *= len(tasks)
    if agent.config.wall_time_limit_seconds > 0:
        agent.config.wall_time_limit_seconds *= len(tasks)


def _continue_turn(task: str) -> dict:
    previous_exit = agent.messages.pop()
    previous = agent.messages[-1] if agent.messages else {}
    actions = previous.get("extra", {}).get("actions", [])
    if actions:
        # Use the model formatter: Responses requires function_call_output, not role=tool.
        outputs = [{"output": previous_exit.get("content", ""), "returncode": 0, "exception_info": ""}]
        agent.add_messages(*agent.model.format_observation_messages(previous, outputs, agent.get_template_vars()))
    else:
        agent.add_messages(agent.model.format_message(role="assistant", content=previous_exit.get("content", "")))
    agent.extra_template_vars["task"] = task
    agent.add_messages(agent.model.format_message(role="user", content=task))

    while True:
        try:
            agent.step()
            agent.n_consecutive_format_errors = 0
        except FormatError as e:
            agent.n_consecutive_format_errors += 1
            if 0 < agent.config.max_consecutive_format_errors <= agent.n_consecutive_format_errors:
                agent.add_messages(*e.messages, {
                    "role": "exit",
                    "content": "RepeatedFormatError",
                    "extra": {"exit_status": "RepeatedFormatError", "submission": ""},
                })
            else:
                agent.add_messages(*e.messages)
        except InterruptAgentFlow as e:
            agent.add_messages(*e.messages)
        except Exception as e:
            agent.handle_uncaught_exception(e)
            raise
        finally:
            agent.save(agent.config.output_path, {"multi_turn": {"turn_count": len(tasks)}})
        if agent.messages[-1].get("role") == "exit":
            return agent.messages[-1].get("extra", {})


try:
    info = agent.run(tasks[0])
    for next_task in tasks[1:]:
        if info.get("exit_status") != "Submitted":
            break  # Stop subsequent turns after a failed turn.
        info = _continue_turn(next_task)
    agent.save(agent.config.output_path, {"multi_turn": {"turn_count": len(tasks)}})
except Exception as e:  # DefaultAgent re-raises after saving the traj; still emit a status line
    info = {"exit_status": type(e).__name__, "submission": ""}
print(json.dumps({"exit_status": info.get("exit_status", ""), "submission": info.get("submission", "")}))
