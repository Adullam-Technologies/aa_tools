"""News headlines from NewsAPI."""

from __future__ import annotations

from ._http import request
from ._util import require_key, truncate

NEWS_API = "https://newsapi.org/v2"


def get_news(query: str, api_key: str, *, count: int = 5, sort: str = "popularity"):
    """Search recent news articles about a topic.

    Parameters
    ----------
    query : str
        Topic to search, e.g. ``"climate change"``.
    api_key : str
        NewsAPI key (https://newsapi.org/).
    count : int
        Number of articles (1-100).
    sort : str
        ``"popularity"``, ``"relevancy"`` or ``"publishedAt"``.

    Returns
    -------
    list[dict]
        Each has ``title``, ``source``, ``url`` and ``snippet``.

    Example
    -------
    >>> for article in aa.get_news("robots", api_key="YOUR_KEY"):
    ...     print(article["title"])
    """
    require_key(api_key, "api_key")
    data = request(
        f"{NEWS_API}/everything",
        params={
            "q": query,
            "pageSize": min(max(count, 1), 100),
            "sortBy": sort,
            "language": "en",
        },
        headers={"X-Api-Key": api_key},
    )
    return [
        {
            "title": a.get("title", ""),
            "source": (a.get("source") or {}).get("name", ""),
            "url": a.get("url", ""),
            "snippet": truncate(a.get("description", ""), 300),
        }
        for a in data.get("articles", [])
    ]


def top_headlines(api_key: str, *, country: str = "us", count: int = 5):
    """Get today's top headlines for a country (default: US)."""
    require_key(api_key, "api_key")
    data = request(
        f"{NEWS_API}/top-headlines",
        params={"country": country, "pageSize": min(max(count, 1), 100)},
        headers={"X-Api-Key": api_key},
    )
    return [
        {
            "title": a.get("title", ""),
            "source": (a.get("source") or {}).get("name", ""),
            "url": a.get("url", ""),
            "snippet": truncate(a.get("description", ""), 300),
        }
        for a in data.get("articles", [])
    ]
