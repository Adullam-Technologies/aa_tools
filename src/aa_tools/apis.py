"""Connect to any API with an API key (and talk to AI models).

These are the "give my agent super-powers" functions. Most web APIs just need
a GET/POST request plus a key - :func:`call_api` does that for you.
"""

from __future__ import annotations

from ._http import request
from ._util import require_key


def call_api(
    url: str,
    api_key: str | None = None,
    *,
    method: str = "GET",
    params: dict | None = None,
    json_body: dict | None = None,
    extra_headers: dict | None = None,
    key_header: str = "Authorization",
    key_prefix: str = "Bearer ",
):
    """Call almost any REST API in one line.

    Parameters
    ----------
    url : str
        The full API endpoint, e.g. ``"https://api.example.com/v1/things"``.
    api_key : str | None
        Your key. It is sent in the header ``key_header`` with ``key_prefix``.
    method : str
        ``"GET"``, ``"POST"``, etc.
    params : dict | None
        Query-string arguments (for GET requests).
    json_body : dict | None
        JSON body (for POST/PUT requests).
    key_header, key_prefix : str, str
        How to send the key. Many APIs use ``"Bearer "``; some use
        ``key_header="x-api-key"`` with ``key_prefix=""``.

    Example
    -------
    >>> data = aa.call_api(
    ...     "https://api.github.com/repos/octocat/Hello-World",
    ...     key_header="Accept",
    ...     key_prefix="application/vnd.github+json",
    ... )
    >>> print(data["stargazers_count"])
    """
    headers = dict(extra_headers or {})
    if api_key:
        headers[key_header] = f"{key_prefix}{api_key}"
    return request(
        url,
        method=method,
        params=params,
        json_body=json_body,
        headers=headers,
    )
