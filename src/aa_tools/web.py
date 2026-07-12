"""Search the web and read web pages.

These functions need a Brave Search API key (get a free one at
https://brave.com/search/api/). The key is never stored - you pass it each
time you call the function.
"""

from __future__ import annotations

import html
import re

from ._http import request
from ._util import require_key, truncate

BRAVE_SEARCH_URL = "https://api.search.brave.com/res/v1/web/search"
JINA_READER = "https://r.jina.ai/"


def search_web(query: str, api_key: str, count: int = 5, country: str = "US"):
    """Search the web with Brave and get back a tidy list of results.

    Parameters
    ----------
    query : str
        What to search for, e.g. ``"best robots for kids"``.
    api_key : str
        Your Brave Search API subscription token.
    count : int
        How many results to return (1-20).
    country : str
        Two-letter country code, e.g. ``"US"`` or ``"GB"``.

    Returns
    -------
    list[dict]
        Each item has ``title``, ``url`` and ``snippet``.

    Example
    -------
    >>> results = aa.search_web("how do dolphins sleep", api_key="YOUR_KEY")
    >>> for r in results:
    ...     print(r["title"], "->", r["url"])
    """
    require_key(api_key, "api_key")
    data = request(
        BRAVE_SEARCH_URL,
        params={
            "q": query,
            "count": min(max(count, 1), 20),
            "country": country,
            "search_lang": "en",
            "result_filter": "web",
        },
        headers={
            "Accept": "application/json",
            "X-Subscription-Token": api_key,
        },
    )
    web = (data.get("web") or {}).get("results") or []
    return [
        {
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "snippet": truncate(item.get("description", ""), 400),
        }
        for item in web
    ]


def search_images(query: str, api_key: str, count: int = 5):
    """Search for images on the web with Brave (needs an API key)."""
    require_key(api_key, "api_key")
    data = request(
        BRAVE_SEARCH_URL,
        params={"q": query, "count": min(max(count, 1), 20), "result_filter": "images"},
        headers={"Accept": "application/json", "X-Subscription-Token": api_key},
    )
    imgs = (data.get("images") or {}).get("results") or []
    return [
        {
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "thumbnail": (item.get("thumbnail") or {}).get("src", ""),
        }
        for item in imgs
    ]


def fetch_page(url: str, *, use_reader: bool = True, max_chars: int = 8000):
    """Download a web page and return its text (as Markdown when possible).

    By default this uses the free Jina Reader service to turn the page into
    clean Markdown. Set ``use_reader=False`` to strip the HTML yourself.

    Example
    -------
    >>> text = aa.fetch_page("https://en.wikipedia.org/wiki/Penguin")
    >>> print(text[:300])
    """
    if use_reader:
        target = JINA_READER + url if not url.startswith("http") else JINA_READER + url
        try:
            return truncate(request(target, as_json=False), max_chars)
        except Exception:
            pass
    return truncate(_strip_html(_get_html(url)), max_chars)


def _get_html(url: str) -> str:
    return request(url, as_json=False)


def _strip_html(raw: str) -> str:
    # Very small, dependency-free HTML-to-text cleaner.
    raw = re.sub(r"(?is)<script.*?</script>", " ", raw)
    raw = re.sub(r"(?is)<style.*?</style>", " ", raw)
    raw = re.sub(r"(?is)<head.*?</head>", " ", raw)
    raw = re.sub(r"(?is)<!--.*?-->", " ", raw)
    raw = re.sub(r"(?is)<[^>]+>", " ", raw)
    raw = html.unescape(raw)
    raw = re.sub(r"[ \t]+", " ", raw)
    raw = re.sub(r"\n\s*\n\s*\n+", "\n\n", raw)
    return raw.strip()
