"""reportkit — small helpers for rendering tabular run reports."""

__version__ = "1.0.0"


def render(rows):
    """Render a list of (label, value) rows as aligned text lines."""
    width = max((len(str(label)) for label, _ in rows), default=0)
    return "\n".join(f"{str(label):<{width}}  {value}" for label, value in rows)
