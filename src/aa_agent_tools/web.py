"""Search the web and read web pages.

These functions need a Brave Search API key (get a free one at
https://brave.com/search/api/). The key is never stored - you pass it each
time you call the function.
"""

from __future__ import annotations

import html
import re

from ._http import request
from ._util import require_key

JINA_READER = "https://r.jina.ai/"


def search_web(query: str, api_key: str):
    """Search the web with Brave"""
    require_key(api_key, "api_key")
    data = request(
        "https://api.search.brave.com/res/v1/llm/context",
        params={
            "q": query,
            "country": "CA",
            "search_lang": "en",
        },
        headers={
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": api_key,
        },
    )
    
    return data


def search_images(query: str, api_key: str, count: int = 5):
    """Search for images on the web with Brave (needs an API key)."""
    require_key(api_key, "api_key")
    data = request(
        "https://api.search.brave.com/res/v1/images/search",
        params={"q": query, "count": min(max(count, 1), 20)},
        headers={"Accept": "application/json", "Accept-Encoding": "gzip", "X-Subscription-Token": api_key},
    )
    return data.get("results") or []


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
        target = JINA_READER + url
        try:
            res = request(target).get("content") or ""
            if len(res.strip()) > 0:
                return res
        except Exception:
            pass
    return _strip_html(_get_html(url))


def _get_html(url: str) -> str:
    return request(url).get("content") or ""


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
