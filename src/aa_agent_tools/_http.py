"""Internal HTTP helpers for aa_agent_tools.

Everything here uses only the Python standard library so it works inside a
Pyodide (WebAssembly) environment where third-party wheels like ``requests``
may not be available.
"""

from __future__ import annotations

import gzip
import json
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_TIMEOUT = 30
DEFAULT_USER_AGENT = "aa_agent_tools/0.1 (+https://github.com/Adullam-Technologies/aa_agent_tools)"


def build_url(base: str, params: dict | None = None) -> str:
    """Add query-string ``params`` to ``base`` if any are given."""
    if not params:
        return base
    clean = {k: v for k, v in params.items() if v is not None}
    if not clean:
        return base
    sep = "&" if "?" in base else "?"
    return base + sep + urllib.parse.urlencode(clean, doseq=True)


def request(
    url: str,
    method: str = "GET",
    *,
    params: dict | None = None,
    headers: dict | None = None,
    data: bytes | None = None,
    json_body: dict | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict:
    """Make an HTTP request and return parsed JSON (or text).

    Raises
    ------
    AARequestError
        When the server returns an HTTP error status.
    AAError
        For other network / parsing problems.
    """
    from .errors import AAError, AARequestError

    full_url = build_url(url, params)
    merged = {"User-Agent": DEFAULT_USER_AGENT}
    if headers:
        merged.update({k: str(v) for k, v in headers.items()})

    if json_body is not None:
        data = json.dumps(json_body).encode("utf-8")
        merged.setdefault("Content-Type", "application/json")
        merged.setdefault("Accept", "application/json")

    req = urllib.request.Request(full_url, data=data, method=method.upper(), headers=merged)

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw_bytes = resp.read()
            # Auto-decompress if the server sent gzip content
            if resp.headers.get("Content-Encoding") == "gzip":
                raw_bytes = gzip.decompress(raw_bytes)
            raw = raw_bytes.decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:  # status code >= 400
        body = ""
        try:
            raw_bytes = exc.read()
            if exc.headers.get("Content-Encoding") == "gzip":
                raw_bytes = gzip.decompress(raw_bytes)
            body = raw_bytes.decode("utf-8", errors="replace")
        except Exception:
            pass
        raise AARequestError(exc.code, exc.reason, body) from exc
    except urllib.error.URLError as exc:
        raise AAError(f"Could not reach {full_url}: {exc.reason}") from exc

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Some endpoints return plain text; hand it back as-is.
        return { "content": raw }
