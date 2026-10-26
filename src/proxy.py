"""Route model requests using configs/models/ and log exchanges as JSONL.

Provider credentials stay on the host; run tokens correlate proxy records with
runner outputs. Unknown models use the configured vLLM upstream."""

import json
import os
import socket
import time
from pathlib import Path

import aiohttp
import typer
import yaml
from aiohttp import web

_DROP_REQ = {"host", "content-length", "authorization", "x-api-key", "connection",
             "transfer-encoding", "accept-encoding"}
_DROP_RESP = {"content-length", "content-encoding", "transfer-encoding", "connection"}
_ROOT = Path(__file__).resolve().parents[1]
_MODELS_DIR = _ROOT / "configs" / "models"

_PROVIDERS = {
    "openrouter": ("https://openrouter.ai/api", "bearer", "openrouter_key"),
    "openai": ("https://api.openai.com", "bearer", "openai_key"),
    "anthropic": ("https://api.anthropic.com", "x-api-key", "anthropic_key"),
    "dashscope": ("https://dashscope.aliyuncs.com/compatible-mode", "bearer", "dashscope_key"),
}
_DEFAULT_PROVIDER = "vllm"

_LITELLM_PREFIXES = {"openai", "anthropic", "hosted_vllm", "openrouter", "azure", "azure_ai", "vertex_ai",
                     "gemini", "bedrock", "mistral", "cohere", "groq", "together_ai", "fireworks_ai",
                     "deepseek", "xai", "ollama", "perplexity", "litellm_proxy"}
_S: dict = {}


def _wire_name(model_name: str) -> str:
    """The model string that actually reaches the proxy."""
    head, _, rest = model_name.partition("/")
    return rest if rest and head in _LITELLM_PREFIXES else model_name


def _load_providers() -> dict:
    """Map wire model names to providers; reload by restarting the proxy."""
    mp = {}
    for f in sorted(_MODELS_DIR.glob("*.yaml")):
        try:
            y = yaml.safe_load(f.read_text()) or {}
        except Exception:
            continue
        provider, name = y.get("provider"), (y.get("model") or {}).get("model_name", "")
        if provider and name:
            mp[_wire_name(name)] = provider
    return mp


def _host_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))  # no packets sent; just selects the outbound interface
        return s.getsockname()[0]
    finally:
        s.close()


def _route(model) -> tuple[str, str, str]:
    """Return upstream, auth scheme, and credential; unknown models use vLLM."""
    provider = _S["model_provider"].get(model or "", _DEFAULT_PROVIDER)
    if provider in _PROVIDERS:
        upstream, auth, key = _PROVIDERS[provider]
        return upstream, auth, _S[key]
    return _S["vllm_upstream"], "bearer", _S["vllm_key"]


async def _handle(request: web.Request) -> web.StreamResponse:
    body = await request.read()
    req = _json_or_text(body)
    upstream, auth, key = _route(req.get("model") if isinstance(req, dict) else None)
    # Route GPT Messages requests through OpenRouter; OpenAI lacks this endpoint.
    oai_messages = upstream == _PROVIDERS["openai"][0] and request.path_qs.startswith("/v1/messages")
    if oai_messages:
        upstream, auth, key = _PROVIDERS["openrouter"][0], "bearer", _S["openrouter_key"]
    send_body = body
    if isinstance(req, dict):
        model = str(req.get("model", ""))
        mutated, changed = dict(req), False
        if model and upstream.startswith("https://openrouter.ai") and "/" not in model:
            mutated["model"] = ("openai/" if oai_messages else "anthropic/") + model; changed = True
        # Restore reasoning signatures dropped by Codex.
        if request.path.endswith("/responses") and isinstance(mutated.get("input"), list):
            known, fixed, n = _S["sigs"].get(_token(request), {}), [], 0
            for it in mutated["input"]:
                if isinstance(it, dict) and it.get("type") == "reasoning" and not it.get("signature") and it.get("id") in known:
                    it, n = {**it, **known[it["id"]]}, n + 1
                fixed.append(it)
            if n:
                mutated["input"], changed, request["sig_reattached"] = fixed, True, n
        if changed:
            send_body = json.dumps(mutated).encode()
    headers = {k: v for k, v in request.headers.items() if k.lower() not in _DROP_REQ}
    headers["accept-encoding"] = "identity"  # force uncompressed so we can tee/parse the body
    headers.setdefault("anthropic-version", "2023-06-01")
    headers["authorization" if auth == "bearer" else "x-api-key"] = f"Bearer {key}" if auth == "bearer" else key
    t0 = time.time()
    buf = bytearray()  # Retain partial output for error logging.
    up_status = 502
    try:
        async with _S["session"].request(request.method, upstream + request.path_qs,
                                          data=send_body or None, headers=headers) as up:
            up_status = up.status
            resp = web.StreamResponse(status=up.status,
                                      headers={k: v for k, v in up.headers.items() if k.lower() not in _DROP_RESP})
            await resp.prepare(request)
            gone = False
            async for chunk in up.content.iter_any():
                buf += chunk  # Drain upstream even if the client disconnects.
                if not gone:
                    try:
                        await resp.write(chunk)
                    except (aiohttp.ClientError, ConnectionResetError):
                        gone = True
            if not gone:
                try:
                    await resp.write_eof()
                except (aiohttp.ClientError, ConnectionResetError):
                    pass
            if up_status == 200 and request.path.endswith("/responses"):
                _remember_sigs(_token(request), bytes(buf))
            _log(request, req, up_status, _parse_resp(bytes(buf)), time.time() - t0)
            return resp
    except aiohttp.ClientError as e:
        _log(request, req, up_status, _parse_resp(bytes(buf)) if buf else {"error": str(e)}, time.time() - t0)
        return web.json_response({"type": "error", "error": {"type": "proxy_error", "message": str(e)}}, status=502)


def _token(request: web.Request) -> str:
    """Extract the run token used to correlate proxy records."""
    return request.headers.get("Authorization", "").removeprefix("Bearer ") or request.headers.get("x-api-key", "")


def _log(request: web.Request, req, status: int, resp, dt: float) -> None:
    rec = {"ts": round(time.time(), 3), "token": _token(request), "method": request.method,
           "path": request.path, "status": status, "duration_s": round(dt, 3), "request": req, "response": resp}
    if n := request.get("sig_reattached"):
        rec["sig_reattached"] = n
    with _S["log"].open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")


def _reasoning_sigs(raw: bytes) -> dict:
    """Collect reasoning signatures from JSON or SSE Responses replies.

    Codex drops these fields when replaying Claude reasoning; retain them by run
    token so _handle can restore them for OpenRouter."""
    obj, items = _json_or_text(raw), []
    if isinstance(obj, dict):
        items = obj.get("output") or []
    else:
        for line in obj.splitlines():
            if not line.startswith("data:"):
                continue
            try:
                ev = json.loads(line[5:].strip())
            except ValueError:
                continue
            if ev.get("type") == "response.output_item.done":
                items.append(ev.get("item") or {})
            elif ev.get("type") in ("response.completed", "response.incomplete"):
                items += (ev.get("response") or {}).get("output") or []
    return {it["id"]: {k: it[k] for k in ("signature", "format") if k in it}
            for it in items if isinstance(it, dict) and it.get("type") == "reasoning" and it.get("id") and it.get("signature")}


def _remember_sigs(token: str, raw: bytes) -> None:
    if sigs := _reasoning_sigs(raw):
        store = _S["sigs"]
        store.setdefault(token, {}).update(sigs)
        while len(store) > 512:  # bound memory: forget the oldest run's signatures
            del store[next(iter(store))]


def build_traj(req: dict, resp) -> dict:
    """Assemble one exchange into the enriched proxy trajectory (request config + tools + full messages)."""
    return {"request_config": {k: v for k, v in req.items() if k not in ("messages", "input", "tools")},
            "tools": req.get("tools", []),
            "messages": (req.get("messages") or req.get("input") or []) + [resp]}


def _json_or_text(raw: bytes):
    try:
        return json.loads(raw)
    except ValueError:
        return raw.decode("utf-8", "replace")


def _parse_resp(raw: bytes):
    """Parse JSON or reassemble Messages, Chat Completions, and Responses SSE replies."""
    obj = _json_or_text(raw)
    if isinstance(obj, dict):
        return obj
    return (_sse_anthropic(obj) or _sse_openai_chat(obj) or _sse_openai_responses(obj)
            or {"raw_sse": obj[:20000]})


def _sse_anthropic(text: str):
    """Anthropic Messages SSE -> {content:[text|thinking|tool_use], stop_reason, usage}; None if not this shape."""
    blocks, stop, usage, saw = {}, None, None, False
    for line in text.splitlines():
        if not line.startswith("data:"):
            continue
        try:
            ev = json.loads(line[5:].strip())
        except ValueError:
            continue
        typ, i = ev.get("type"), ev.get("index")
        if typ == "content_block_start":
            blocks[i], saw = {**ev.get("content_block", {}), "_j": ""}, True
        elif typ == "content_block_delta":
            d, b, saw = ev.get("delta", {}), blocks.setdefault(i, {"type": "text", "_j": ""}), True
            if d.get("type") == "text_delta":
                b["text"] = b.get("text", "") + d.get("text", "")
            elif d.get("type") == "thinking_delta":
                b["thinking"] = b.get("thinking", "") + d.get("thinking", "")
            elif d.get("type") == "input_json_delta":
                b["_j"] += d.get("partial_json", "")
        elif typ == "message_delta":
            stop, usage, saw = ev.get("delta", {}).get("stop_reason", stop), ev.get("usage", usage), True
    if not saw:
        return None
    content = []
    for i in sorted(blocks):
        b = blocks[i]
        if (j := b.pop("_j", "")) and b.get("type") == "tool_use":
            b["input"] = _json_or_text(j.encode())
        content.append(b)
    return {"content": content, "stop_reason": stop, "usage": usage}


def _sse_openai_chat(text: str):
    """OpenAI chat-completions SSE -> {content, tool_calls, finish_reason, usage}; None if not this shape."""
    content, tools, finish, usage, saw = "", {}, None, None, False
    for line in text.splitlines():
        if not line.startswith("data:") or line[5:].strip() == "[DONE]":
            continue
        try:
            ev = json.loads(line[5:].strip())
        except ValueError:
            continue
        usage = ev.get("usage") or usage
        for ch in ev.get("choices", []):
            saw, d = True, ch.get("delta", {})
            content += d.get("content") or ""
            finish = ch.get("finish_reason") or finish
            for tc in d.get("tool_calls") or []:
                t = tools.setdefault(tc.get("index", 0), {"id": tc.get("id", ""), "name": "", "arguments": ""})
                t["name"] = tc.get("function", {}).get("name") or t["name"]
                t["arguments"] += tc.get("function", {}).get("arguments") or ""
    if not saw:
        return None
    out = {"content": content, "finish_reason": finish, "usage": usage}
    if tools:
        out["tool_calls"] = [{**tools[k], "arguments": _json_or_text(tools[k]["arguments"].encode())} for k in sorted(tools)]
    return out


def _sse_openai_responses(text: str):
    """Parse Responses SSE, preferring the terminal output array.

    If the stream ends early, retain accumulated text and tool-call deltas."""
    body, reasoning, calls, status, usage, final, saw = "", "", {}, None, None, None, False
    for line in text.splitlines():
        if not line.startswith("data:"):
            continue
        try:
            ev = json.loads(line[5:].strip())
        except ValueError:
            continue
        typ = ev.get("type", "")
        if not typ.startswith("response."):
            continue
        saw = True
        if typ == "response.output_text.delta":
            body += ev.get("delta") or ""
        elif typ in ("response.reasoning_summary_text.delta", "response.reasoning_text.delta"):
            reasoning += ev.get("delta") or ""
        elif typ == "response.output_item.added" and ev.get("item", {}).get("type") == "function_call":
            it = ev["item"]
            calls[ev.get("output_index", len(calls))] = {
                "id": it.get("call_id") or it.get("id", ""), "name": it.get("name", ""), "arguments": ""}
        elif typ == "response.function_call_arguments.delta":
            c = calls.setdefault(ev.get("output_index", 0), {"id": ev.get("item_id", ""), "name": "", "arguments": ""})
            c["arguments"] += ev.get("delta") or ""
        elif typ in ("response.completed", "response.incomplete", "response.failed"):
            r = ev.get("response") or {}
            usage, status, final = r.get("usage", usage), r.get("status", status), r.get("output", final)
    if not saw:
        return None
    if final is not None:  # terminal `output` array is authoritative when present
        body, reasoning, calls = "", "", {}
        for it in final:
            t = it.get("type")
            if t == "message":
                body += "".join(p.get("text", "") for p in it.get("content", []) if p.get("type") in ("output_text", "text"))
            elif t == "reasoning":
                reasoning += "".join(p.get("text", "") for p in (it.get("summary", []) + it.get("content", [])))
            elif t == "function_call":
                calls[len(calls)] = {"id": it.get("call_id") or it.get("id", ""),
                                     "name": it.get("name", ""), "arguments": it.get("arguments", "")}
    out = {"content": body, "status": status, "usage": usage}
    if reasoning:
        out["reasoning"] = reasoning
    if calls:
        out["tool_calls"] = [{**calls[k], "arguments": _json_or_text(str(calls[k]["arguments"]).encode())}
                             for k in sorted(calls)]
    return out


def main(port: int = typer.Option(9000, help="listen port"),
         log: Path = typer.Option(_ROOT / "results" / "proxy" / "proxy-default.jsonl", help="JSONL exchange log (appended)")):
    _S.update(log=log, sigs={}, model_provider=_load_providers(), anthropic_key=os.environ.get("ANTHROPIC_API_KEY", ""),
              openai_key=os.environ.get("OPENAI_API_KEY", ""),
              openrouter_key=os.environ.get("OPENROUTER_API_KEY", ""),
              dashscope_key=os.environ.get("DASHSCOPE_API_KEY", ""),
              vllm_upstream=os.environ.get("VLLM_UPSTREAM", "http://localhost:8000"),
              vllm_key=os.environ.get("VLLM_API_KEY", "token-abc123"))
    if base := os.environ.get("DASHSCOPE_BASE_URL"):  # .env may name another region/gateway; drop the /v1 the path carries
        _PROVIDERS["dashscope"] = (base.rstrip("/").removesuffix("/v1"), "bearer", "dashscope_key")
    log.parent.mkdir(parents=True, exist_ok=True)
    app = web.Application(client_max_size=64 * 1024 * 1024)
    app.router.add_route("*", "/{tail:.*}", _handle)

    async def _open(_):
        _S["session"] = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=None, sock_connect=30))

    async def _close(_):
        await _S["session"].close()

    app.on_startup.append(_open)
    app.on_cleanup.append(_close)

    typer.secho(f"logging proxy: 0.0.0.0:{port}   routing {len(_S['model_provider'])} profiles by provider "
                f"(default vLLM {_S['vllm_upstream']})   log -> {log}", bold=True)
    typer.echo(f"point runs at it:  --api-base http://{_host_ip()}:{port}[/v1]  (use run.sh)")
    web.run_app(app, host="0.0.0.0", port=port, print=None)


if __name__ == "__main__":
    typer.run(main)
