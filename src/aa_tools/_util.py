"""Small shared helpers: key checking, text truncation, pretty printing."""

from __future__ import annotations

from .errors import AAMissingKeyError


def require_key(value, name: str):
    """Return ``value`` or raise :class:`AAMissingKeyError` if it is falsy."""
    if not value:
        raise AAMissingKeyError(name)
    return value


def truncate(text: str, limit: int = 600) -> str:
    """Trim ``text`` to ``limit`` characters and add an ellipsis if needed."""
    if text is None:
        return ""
    text = str(text)
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def pretty(obj) -> str:
    """Return a human-friendly, readable string for any result."""
    import json

    if isinstance(obj, (dict, list)):
        try:
            return json.dumps(obj, indent=2, ensure_ascii=False)
        except TypeError:
            pass
    return str(obj)
