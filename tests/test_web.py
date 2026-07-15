"""Tests for aa_agent_tools.web."""

from __future__ import annotations

import pytest

from aa_agent_tools import web
from aa_agent_tools.errors import AAMissingKeyError


class TestSearchWeb:
    def test_requires_api_key(self):
        with pytest.raises(AAMissingKeyError):
            web.search_web("query", "")

    def test_success_returns_llm_context(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({
            "grounding": {
                "generic": [
                    {"url": "https://example.com", "title": "Penguins", "snippets": ["Penguins are birds."]}
                ]
            },
            "sources": {"https://example.com": {"title": "Penguins", "hostname": "example.com"}},
        })
        result = web.search_web("penguins", "test-key")
        assert "grounding" in result
        assert len(result["grounding"]["generic"]) == 1
        assert result["grounding"]["generic"][0]["title"] == "Penguins"
        sent_headers = mock_urlopen.call_args.kwargs["headers"]
        sent_url = mock_urlopen.call_args.kwargs["url"]
        assert sent_headers["X-Subscription-Token"] == "test-key"
        assert "q=penguins" in sent_url

    def test_uses_llm_context_endpoint(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({})
        web.search_web("test", "mykey")
        sent_url = mock_urlopen.call_args.kwargs["url"]
        assert "llm/context" in sent_url

    def test_sends_api_key_header(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({})
        web.search_web("test", "mykey")
        sent_headers = mock_urlopen.call_args.kwargs["headers"]
        assert sent_headers["X-Subscription-Token"] == "mykey"

    def test_sends_country_and_lang_params(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({})
        web.search_web("test", "key")
        sent_url = mock_urlopen.call_args.kwargs["url"]
        assert "country=CA" in sent_url
        assert "search_lang=en" in sent_url


class TestSearchImages:
    def test_requires_api_key(self):
        with pytest.raises(AAMissingKeyError):
            web.search_images("cats", "")

    def test_returns_parsed_images(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({
            "images": {
                "results": [
                    {"title": "Cat 1", "url": "https://cat1.jpg", "thumbnail": {"src": "https://thumb1.jpg"}},
                    {"title": "Cat 2", "url": "https://cat2.jpg", "thumbnail": {"src": "https://thumb2.jpg"}},
                ]
            }
        })
        result = web.search_images("cats", "key")
        assert len(result) == 2
        assert result[0] == {"title": "Cat 1", "url": "https://cat1.jpg", "thumbnail": "https://thumb1.jpg"}

    def test_empty_results(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({})
        result = web.search_images("nothing", "key")
        assert result == []

    def test_count_clamped(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({"images": {"results": []}})
        web.search_images("x", "key", count=100)
        sent_url = mock_urlopen.call_args.kwargs["url"]
        assert "count=20" in sent_url

    def test_count_minimum(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({"images": {"results": []}})
        web.search_images("x", "key", count=0)
        sent_url = mock_urlopen.call_args.kwargs["url"]
        assert "count=1" in sent_url


class TestFetchPage:
    def test_uses_jina_reader_by_default(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({"content": "# Markdown content"})
        result = web.fetch_page("https://example.com")
        assert result == "# Markdown content"
        sent_url = mock_urlopen.call_args.kwargs["url"]
        assert sent_url.startswith("https://r.jina.ai/")

    def test_falls_back_to_html_stripping(self, mock_urlopen, fake_response):
        # First call (Jina) fails, second (raw HTML) succeeds
        mock_urlopen.side_effect = [Exception("jina down"), fake_response({"content": "<html><body>Hello</body></html>"})]
        result = web.fetch_page("https://example.com", use_reader=True)
        assert "Hello" in result
        assert "<html>" not in result

    def test_strip_html_directly(self):
        raw = "<html><head><title>T</title></head><body><p>Hello &amp; bye</p></body></html>"
        result = web._strip_html(raw)
        assert "Hello & bye" in result
        assert "<" not in result

    def test_no_reader_mode(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({"content": "<html><body>Plain</body></html>"})
        result = web.fetch_page("https://example.com", use_reader=False)
        assert "Plain" in result


class TestStripHtml:
    def test_removes_scripts(self):
        raw = "<script>alert('x')</script>hello"
        assert "alert" not in web._strip_html(raw)
        assert "hello" in web._strip_html(raw)

    def test_removes_styles(self):
        raw = "<style>body{color:red}</style>text"
        assert "color" not in web._strip_html(raw)
        assert "text" in web._strip_html(raw)

    def test_unescapes_entities(self):
        raw = "&lt;p&gt;text&lt;/p&gt;"
        assert "<p>text</p>" == web._strip_html(raw)

    def test_collapses_whitespace(self):
        raw = "a\n\n\n\n\nb"
        result = web._strip_html(raw)
        assert "\n\n\n" not in result