"""Render versioned maintainer templates for the local notification/report tool."""
from pathlib import Path
TEMPLATE_DIR = Path(__file__).resolve().parents[1] / 'templates'

def render_message(recipient: str, template_name: str) -> str:
    """Return the complete rendered local template; see README.md."""
    raise NotImplementedError('implement local template rendering')
