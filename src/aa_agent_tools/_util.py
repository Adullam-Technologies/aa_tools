"""Small shared helpers: key checking, text truncation, pretty printing, URL encoding."""

from __future__ import annotations

from .errors import AAMissingKeyError


def require_key(value, name: str):
    """Return ``value`` or raise :class:`AAMissingKeyError` if it is falsy."""
    if not value:
        raise AAMissingKeyError(name)
    return value



def pretty(obj) -> str:
    """Return a human-friendly, readable string for any result."""
    import json

    if isinstance(obj, (dict, list)):
        try:
            return json.dumps(obj, indent=2, ensure_ascii=False)
        except TypeError:
            pass
    return str(obj)


# ---- tiny dependency-free URL encoding -----------------------------------
# RFC 3986 "unreserved" characters that never need percent-encoding.
_UNRESERVED = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~"
)


def quote(value) -> str:
    """Percent-encode ``value`` for safe use in a URL (like ``urllib.parse.quote``)."""
    if not isinstance(value, str):
        value = str(value)
    out = []
    for byte in value.encode("utf-8"):
        ch = chr(byte)
        if ch in _UNRESERVED:
            out.append(ch)
        else:
            out.append(f"%{byte:02X}")
    return "".join(out)


def urlencode(query: dict, *, doseq: bool = False) -> str:
    """Encode a mapping into a ``key=value&key=value`` query string.

    ``None`` values are skipped. When ``doseq`` is true, list/tuple values are
    emitted as one ``key=item`` pair per item.
    """
    pairs = []
    for key, val in query.items():
        if val is None:
            continue
        if doseq and isinstance(val, (list, tuple)):
            for item in val:
                pairs.append(f"{quote(key)}={quote(item)}")
        else:
            pairs.append(f"{quote(key)}={quote(val)}")
    return "&".join(pairs)
