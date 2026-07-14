"""Live tests for keyless public APIs in aa_agent_tools.

These make real network calls but need no API keys, so they can run whenever
``--live`` is passed (even without a .env file). Run with::

    uv run pytest --live -m live tests/test_free_apis_live.py
"""

from __future__ import annotations

import pytest

from aa_agent_tools import fun, data, space


pytestmark = pytest.mark.live


class TestFunLive:
    def test_get_joke(self):
        result = fun.get_joke()
        assert isinstance(result, dict)
        assert result["setup"]
        assert result["punchline"]

    def test_get_cat_fact(self):
        result = fun.get_cat_fact()
        assert isinstance(result, str)
        assert len(result) > 10

    def test_get_dog_image(self):
        result = fun.get_dog_image()
        assert result.startswith("http")

    def test_get_quote(self):
        result = fun.get_quote()
        assert result["text"]
        assert result["author"]

    def test_get_advice(self):
        result = fun.get_advice()
        assert isinstance(result, str)
        assert len(result) > 5

    def test_get_pokemon(self):
        result = fun.get_pokemon("pikachu")
        assert result["name"] == "pikachu"
        assert "electric" in result["types"]
        assert result["sprite"]


class TestDataLive:
    def test_wikipedia_summary(self):
        result = data.wikipedia_summary("Penguin")
        assert result["title"]
        assert result["summary"]
        assert "wikipedia.org" in result["url"]

    def test_define_word(self):
        result = data.define_word("hello")
        assert result["word"] == "hello"
        assert len(result["definitions"]) > 0

    def test_convert_money(self):
        result = data.convert_money(10, "USD", "EUR")
        if result is not None:  # rate service can be flaky
            assert isinstance(result, (int, float))
            assert result > 0

    def test_shorten_url(self):
        result = data.shorten_url("https://example.com/some/very/long/path")
        assert result.startswith("http")


class TestSpaceLive:
    def test_space_image(self):
        try:
            result = space.space_image()
        except Exception as exc:
            # DEMO_KEY has low rate limits (30/hr) — skip on 429
            if "429" in str(exc) or "rate" in str(exc).lower():
                pytest.skip(f"NASA DEMO_KEY rate-limited: {exc}")
            raise
        assert result["title"]
        assert result["url"]