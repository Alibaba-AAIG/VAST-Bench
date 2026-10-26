#!/usr/bin/env python3
"""Interactive inspector for proxy_traj.json captures (modeled on mini-extra's inspector).

A proxy_traj.json is the raw wire payload of one LLM API call recorded by the host
proxy: {request_config, tools, messages}. Its shape depends on the scaffold's API
dialect (mini = OpenAI chat-completions, claude-code = Anthropic messages, codex =
OpenAI responses). This tool auto-detects the dialect, normalises it, and shows only
the meaningful content -- system prompt, user task, model text, the commands the model
issued and their output -- dropping tool schemas, telemetry, call ids and token usage.

Usage:
    python src/proxy_inspector.py path/to/proxy_traj.json      # TUI (keyboard navigation)
    python src/proxy_inspector.py <dir>                        # all proxy_traj.json under it
    python src/proxy_inspector.py <path> --print [--full]      # plain terminal output

Keys: left/right = step, 0/$ = first/last, j/k = scroll, H/L = file, q = quit.
"""

import json
from dataclasses import dataclass
from pathlib import Path

import typer
from rich.console import Console
from rich.rule import Rule
from rich.text import Text
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical, VerticalScroll
from textual.widgets import Footer, Header, Static

app = typer.Typer(rich_markup_mode="rich", add_completion=False)
console = Console()


@dataclass
class Event:
    kind: str  # system | user | assistant | tool_call | tool_output
    text: str = ""
    tool: str = ""  # tool name (tool_call only)


# Normalize API dialects into events.


def _cmd_of(args) -> str:
    """Extract the effective command/argument string from a tool-call payload."""
    if isinstance(args, str):
        try:
            args = json.loads(args)
        except json.JSONDecodeError:
            return args
    if isinstance(args, dict):
        return args.get("command") or args.get("cmd") or json.dumps(args, ensure_ascii=False)
    return str(args)


def _text_of(content) -> str:
    """Join the text of an Anthropic/Responses-style content list (or pass a string through)."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(b["text"] for b in content if isinstance(b, dict) and b.get("type", "").endswith("text"))
    return ""


def _strip_codex_header(out: str) -> str:
    """Codex tool output is prefixed with Chunk ID / Wall time / token-count metadata."""
    marker = "\nOutput:\n"
    return out.split(marker, 1)[1] if marker in out else out


def _detect(data: dict) -> tuple[str, str]:
    """Return (scaffold, dialect): who made the call, and which wire format it used."""
    tools = data.get("tools") or []
    t0 = tools[0] if tools else {}
    msgs = data.get("messages") or []
    resp_types = {"reasoning", "function_call", "function_call_output"}
    is_responses = "instructions" in data.get("request_config", {}) or any(
        isinstance(m, dict) and (m.get("type") in resp_types or isinstance(m.get("output"), list)) for m in msgs)
    if is_responses:
        names = [t.get("name") or t.get("function", {}).get("name") for t in tools]
        scaffold = "mini" if names == ["bash"] else "codex"
        return scaffold, "responses"
    if "input_schema" in t0:
        return "claude-code", "anthropic"
    if "function" in t0:
        return "mini", "chat"
    return "mini", "chat"


def normalize(data: dict) -> tuple[str, str, str, list[Event]]:
    """Return (scaffold, model, system_text, events) for any of the three dialects."""
    rc = data.get("request_config", {})
    model = rc.get("model", "?")
    scaffold, dialect = _detect(data)
    events: list[Event] = []
    system = ""

    if dialect == "anthropic":
        system = _text_of(rc.get("system", ""))
        for m in data["messages"]:
            role, content = m.get("role"), m.get("content")
            if role is None and "stop_reason" in m:  # trailing raw Anthropic response object
                role = "assistant"
            if role is None:
                continue
            if isinstance(content, list):
                for b in content:
                    t = b.get("type")
                    if t == "text":
                        events.append(Event(role, b["text"]))
                    elif t == "thinking" and b.get("thinking"):
                        events.append(Event(role, b["thinking"]))
                    elif t == "tool_use":
                        events.append(Event("tool_call", tool=b["name"], text=_cmd_of(b.get("input"))))
                    elif t == "tool_result":
                        events.append(Event("tool_output", text=_text_of(b.get("content"))))
            elif content:
                events.append(Event(role, content))

    elif dialect == "responses":
        system = rc.get("instructions", "")
        messages = []
        for m in data["messages"]:  # a non-streamed reply carries its items in `output`
            messages += m["output"] if m.get("type") is None and isinstance(m.get("output"), list) else [m]
        for m in messages:
            typ, role = m.get("type"), m.get("role")
            if typ == "function_call":
                events.append(Event("tool_call", tool=m.get("name", ""), text=_cmd_of(m.get("arguments"))))
            elif typ == "function_call_output":
                events.append(Event("tool_output", text=_strip_codex_header(_text_of(m.get("output", "")))))
            elif typ == "reasoning":
                if text := _text_of(m.get("summary", []) + m.get("content", [])):
                    events.append(Event("assistant", text))
            elif role in ("developer", "user", "assistant"):
                events.append(Event("system" if role == "developer" else role, _text_of(m.get("content"))))
            elif role is None and typ is None and m.get("content") is not None:
                # Reassembled Responses SSE reply.
                if m.get("content"):
                    events.append(Event("assistant", _text_of(m.get("content"))))
                for tc in m.get("tool_calls") or []:
                    events.append(Event("tool_call", tool=tc.get("name", ""), text=_cmd_of(tc.get("arguments"))))

    else:  # chat -- OpenAI chat-completions
        for m in data["messages"]:
            role = m.get("role")
            if role is None and "choices" in m:  # trailing raw response object
                m = m["choices"][0]["message"]
                role = "assistant"
            if role == "system":
                system = system or _text_of(m.get("content"))
            elif role == "user":
                events.append(Event("user", _text_of(m.get("content"))))
            elif role == "tool":
                events.append(Event("tool_output", text=_text_of(m.get("content"))))
            elif role == "assistant":
                if m.get("content"):
                    events.append(Event("assistant", m["content"]))
                for tc in m.get("tool_calls") or []:
                    fn = tc.get("function", {})
                    events.append(Event("tool_call", tool=fn.get("name", ""), text=_cmd_of(fn.get("arguments"))))

    return scaffold, model, system, events


def _split_output(events: list[Event]) -> int:
    """Index where this turn's model output starts (final run of assistant/tool_call events)."""
    split = len(events)
    for i in range(len(events) - 1, -1, -1):
        if events[i].kind in ("assistant", "tool_call"):
            split = i
        else:
            break
    return split


def _events_to_steps(events: list[Event]) -> list[list[Event]]:
    """Group events into pages: a new step starts at each assistant turn."""
    steps: list[list[Event]] = []
    current: list[Event] = []
    prev = ""
    for e in events:
        new_turn = e.kind == "assistant" or (e.kind == "tool_call" and prev not in ("assistant", "tool_call"))
        if new_turn and current:
            steps.append(current)
            current = []
        current.append(e)
        prev = e.kind
    if current:
        steps.append(current)
    return steps


def _clean_output(e: Event) -> tuple[str, str]:
    """Return (header_suffix, body) with the <returncode>/<output> wrapper stripped."""
    body = e.text.strip("\n")
    rc_label = ""
    if e.kind == "tool_output" and body.startswith("<returncode>"):
        rc, _, rest = body[len("<returncode>"):].partition("</returncode>")
        rc_label = f" rc={rc.strip()}"
        body = rest.replace("<output>", "").replace("</output>", "").strip("\n")
    return rc_label, body


_LABEL = {"system": "SYSTEM", "user": "USER", "assistant": "ASSISTANT",
          "tool_call": "⇒ CMD", "tool_output": "OUTPUT"}


def _header_of(e: Event) -> str:
    rc_label, _ = _clean_output(e)
    return _LABEL.get(e.kind, e.kind.upper()) + (f" [{e.tool}]" if e.kind == "tool_call" and e.tool else rc_label)


# TUI, based on minisweagent.run.utilities.inspector.

CSS = """
#main { height: 1fr; overflow: hidden; }
VerticalScroll { height: 1fr; }
#content { height: auto; padding: 1; }
.event-container { height: auto; margin-bottom: 1; padding: 0 1; }
.event-content { height: auto; padding: 1; background: $surface; }
.hdr-system { background: $secondary; color: $text; padding: 0 1; text-style: bold; }
.hdr-user { background: $success; color: $text; padding: 0 1; text-style: bold; }
.hdr-assistant { background: $accent; color: $text; padding: 0 1; text-style: bold; }
.hdr-tool_call { background: $warning; color: $text; padding: 0 1; text-style: bold; }
.hdr-tool_output { background: $panel; color: $text-muted; padding: 0 1; }
.section-banner { background: $primary; color: $text; padding: 0 1; text-style: bold; margin-bottom: 1; }
Header { dock: top; }
Footer { dock: bottom; }
"""


class ProxyTrajInspector(App):
    CSS = CSS
    BINDINGS = [
        Binding("right,l", "next_step", "Step++"),
        Binding("left,h", "previous_step", "Step--"),
        Binding("0", "first_step", "Step=0"),
        Binding("$", "last_step", "Step=-1"),
        Binding("j,down", "scroll_down", "↓"),
        Binding("k,up", "scroll_up", "↑"),
        Binding("L", "next_trajectory", "File++"),
        Binding("H", "previous_trajectory", "File--"),
        Binding("q", "quit", "Quit"),
    ]

    def __init__(self, files: list[Path]):
        super().__init__()
        self.files = files
        self._i_file = 0
        self._i_step = 0
        self.scaffold = self.model = ""
        self.steps: list[tuple[str, list[Event]]] = []  # (section_label, events)
        self._load()

    def _load(self) -> None:
        path = self.files[self._i_file]
        try:
            data = json.loads(path.read_text())
            scaffold, model, system, events = normalize(data)
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            self.scaffold = self.model = "?"
            self.steps = [("ERROR", [Event("system", f"Cannot parse {path}: {e}")])]
            self._i_step = 0
            return
        self.scaffold, self.model = scaffold, model
        split = _split_output(events)
        steps: list[tuple[str, list[Event]]] = []
        if system:
            steps.append(("SYSTEM PROMPT", [Event("system", system)]))
        steps += [("MODEL INPUT (context)", s) for s in _events_to_steps(events[:split])]
        steps += [("MODEL OUTPUT (this turn)", s) for s in _events_to_steps(events[split:])]
        self.steps = steps or [("EMPTY", [])]
        self._i_step = 0

    @property
    def i_step(self) -> int:
        return self._i_step

    @i_step.setter
    def i_step(self, value: int) -> None:
        if value != self._i_step and self.steps:
            self._i_step = max(0, min(value, len(self.steps) - 1))
            self.query_one(VerticalScroll).scroll_to(y=0, animate=False)
            self.update_content()

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="main"):
            with VerticalScroll():
                yield Vertical(id="content")
        yield Footer()

    def on_mount(self) -> None:
        self.update_content()

    def update_content(self) -> None:
        container = self.query_one("#content", Vertical)
        container.remove_children()
        section, events = self.steps[self._i_step]
        container.mount(Static(section, classes="section-banner"))
        for e in events:
            _, body = _clean_output(e)
            box = Vertical(classes="event-container")
            container.mount(box)
            box.mount(Static(_header_of(e), markup=False, classes=f"hdr-{e.kind}"))
            box.mount(Static(Text(body.replace("\x00", ""), no_wrap=False), classes="event-content"))
        self.title = (
            f"{self.files[self._i_file].parent.name}/{self.files[self._i_file].name} "
            f"[{self.scaffold} · {self.model}] - File {self._i_file + 1}/{len(self.files)} - "
            f"Step {self._i_step + 1}/{len(self.steps)}"
        )

    def action_next_step(self) -> None:
        self.i_step += 1

    def action_previous_step(self) -> None:
        self.i_step -= 1

    def action_first_step(self) -> None:
        self.i_step = 0

    def action_last_step(self) -> None:
        self.i_step = len(self.steps) - 1

    def action_next_trajectory(self) -> None:
        self._switch_file(self._i_file + 1)

    def action_previous_trajectory(self) -> None:
        self._switch_file(self._i_file - 1)

    def _switch_file(self, value: int) -> None:
        value = max(0, min(value, len(self.files) - 1))
        if value != self._i_file:
            self._i_file = value
            self._load()
            self.query_one(VerticalScroll).scroll_to(y=0, animate=False)
            self.update_content()

    def action_scroll_down(self) -> None:
        vs = self.query_one(VerticalScroll)
        vs.scroll_to(y=vs.scroll_target_y + 15)

    def action_scroll_up(self) -> None:
        vs = self.query_one(VerticalScroll)
        vs.scroll_to(y=vs.scroll_target_y - 15)


# Plain terminal output (--print).

_STYLE = {"system": "dim cyan", "user": "bold green", "assistant": "bold blue",
          "tool_call": "yellow", "tool_output": "dim"}


def _emit(e: Event, full: bool, max_lines: int) -> None:
    rc_label, body = _clean_output(e)
    console.print(f"[{_STYLE.get(e.kind, 'white')}]{_header_of(e)}[/]")
    lines = body.splitlines() or [""]
    if not full and len(lines) > max_lines:
        console.print("\n".join(lines[:max_lines]), markup=False, highlight=False)
        console.print(f"[dim]  … (+{len(lines) - max_lines} lines, use --full)[/dim]")
    else:
        console.print(body, markup=False, highlight=False)
    console.print()


def render_print(path: Path, full: bool, max_lines: int) -> None:
    data = json.loads(path.read_text())
    if not (isinstance(data, dict) and "messages" in data):
        console.print(f"[red]{path}: not a proxy_traj.json (missing 'messages')[/red]")
        return
    scaffold, model, system, events = normalize(data)
    split = _split_output(events)
    console.print(Rule(f"[bold]{path.name}[/bold]  scaffold=[magenta]{scaffold}[/magenta]  "
                       f"model=[magenta]{model}[/magenta]  events={len(events)}"))
    if system:
        _emit(Event("system", system), full, max_lines)
    console.print(Rule("[bold]MODEL INPUT (context)[/bold]", style="green"))
    for e in events[:split]:
        _emit(e, full, max_lines)
    console.print(Rule("[bold]MODEL OUTPUT (this turn)[/bold]", style="blue"))
    for e in events[split:]:
        _emit(e, full, max_lines)


@app.command(help=__doc__)
def main(
    path: str = typer.Argument(..., help="A proxy_traj.json file or a directory to search"),
    print_mode: bool = typer.Option(False, "--print", help="Plain terminal output instead of the TUI"),
    full: bool = typer.Option(False, "--full", help="[--print] Do not truncate long blocks"),
    max_lines: int = typer.Option(24, "--max-lines", help="[--print] Max lines per block before truncating"),
) -> None:
    p = Path(path)
    files = [p] if p.is_file() else sorted(p.rglob("proxy_traj.json")) if p.is_dir() else []
    if not files:
        raise typer.BadParameter(f"No proxy_traj.json found at '{path}'")
    if print_mode:
        for f in files:
            render_print(f, full, max_lines)
    else:
        ProxyTrajInspector(files).run()


if __name__ == "__main__":
    app()
