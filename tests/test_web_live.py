"""Live tests for aa_tools.web (Brave Search + Jina Reader).

These make real network calls and need a Brave API key. Run with::

    uv run pytest --live -m live tests/test_web_live.py
"""

from __future__ import annotations

import pytest

from aa_tools import web


pytestmark = pytest.mark.live


class TestSearchWebLive:
    def test_search_returns_grounding_context(self, brave_api_key):
        if not brave_api_key:
            pytest.skip("BRAVE_API_KEY not set")
        data = web.search_web("penguin", brave_api_key)
        assert isinstance(data, dict)
        # LLM Context API returns grounding.generic with extracted content
        generic = data.get("grounding", {}).get("generic") or []
        assert len(generic) > 0
        first = generic[0]
        assert "url" in first
        assert "title" in first
        assert isinstance(first.get("snippets"), list)

    def test_search_images_returns_list(self, brave_api_key):
        if not brave_api_key:
            pytest.skip("BRAVE_API_KEY not set")
        try:
            results = web.search_images("cute cat", brave_api_key, count=3)
        except Exception as exc:
            # The free Brave key may not cover the web/search endpoint
            pytest.skip(f"search_images not available with this key: {exc}")
        assert isinstance(results, list)


class TestFetchPageLive:
    def test_fetch_wikipedia(self):
        text = web.fetch_page("https://en.wikipedia.org/wiki/Penguin")
        assert isinstance(text, str)
        assert len(text) > 100
        # Markdown from Jina reader often contains headings
        assert "penguin" in text.lower()