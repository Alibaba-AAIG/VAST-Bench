"""Tenant report-preview renderer.

Tenants submit their OWN report *template source* (not just values) through the
portal; this module compiles that tenant-supplied template text and renders it
with the tenant's context. Because the template body is attacker-controllable
input, rendering runs inside a Jinja2 ``SandboxedEnvironment`` — the sandbox is
the trust boundary that stops a tenant template from reaching Python internals.

``render_preview(template_source, context)`` compiles the tenant-submitted
template string and renders it with the provided context mapping.
"""
from __future__ import annotations

from jinja2.sandbox import SandboxedEnvironment


def render_preview(template_source: str, context: dict) -> str:
    """Render a tenant-submitted report template.

    ``template_source`` is the raw template text the tenant uploaded (content,
    not just variables), so it is rendered in a sandbox.
    """
    env = SandboxedEnvironment(autoescape=True)
    template = env.from_string(template_source)
    return template.render(**context)
