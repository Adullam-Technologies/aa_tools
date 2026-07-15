"""Internal HTTP helpers for aa_agent_tools.

All HTTP traffic goes through :mod:`urllib3` so we get connection pooling,
automatic gzip/deflate decompression, and consistent error handling across
every API helper in the package.
"""

from __future__ import annotations

import json

import urllib3

from ._util import quote, urlencode

DEFAULT_TIMEOUT = 30

# A single shared :class:`~urllib3.PoolManager` is reused for every request so
# connections can be kept alive and reused across calls.
_pool = urllib3.PoolManager(timeout=DEFAULT_TIMEOUT)


def build_url(base: str, params: dict | None = None) -> str:
    """Add query-string ``params`` to ``base`` if any are given."""
    if not params:
        return base
    clean = {k: v for k, v in params.items() if v is not None}
    if not clean:
        return base
    sep = "&" if "?" in base else "?"
    return base + sep + urlencode(clean, doseq=True)


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
    merged = {}
    if headers:
        merged.update({k: str(v) for k, v in headers.items()})

    body: bytes | None = data
    if json_body is not None:
        body = json.dumps(json_body).encode("utf-8")
        merged.setdefault("Content-Type", "application/json")
        merged.setdefault("Accept", "application/json")

    try:
        resp = _pool.request(
            method=method.upper(),
            url=full_url,
            body=body,
            headers=merged,
            timeout=urllib3.Timeout(total=timeout),
        )
    except urllib3.exceptions.HTTPError as exc:
        raise AAError(f"Could not reach {full_url}: {exc}") from exc

    # ``response.data`` is already decompressed by urllib3 when the server used
    # gzip / deflate / brotli content-encoding.
    raw = (resp.data or b"").decode("utf-8", errors="replace")

    if resp.status >= 400:
        raise AARequestError(resp.status, resp.reason or "", raw)

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Some endpoints return plain text; hand it back as-is.
        return {"content": raw}
