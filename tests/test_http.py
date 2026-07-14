"""Tests for aa_agent_tools._http."""

from __future__ import annotations

import json
import pytest

from aa_agent_tools._http import build_url, request


class TestBuildUrl:
    def test_no_params(self):
        assert build_url("https://example.com") == "https://example.com"

    def test_empty_params(self):
        assert build_url("https://example.com", {}) == "https://example.com"

    def test_none_values_skipped(self):
        assert build_url("https://example.com", {"a": 1, "b": None}) == "https://example.com?a=1"

    def test_all_none(self):
        assert build_url("https://example.com", {"a": None}) == "https://example.com"

    def test_append_no_question(self):
        url = build_url("https://example.com", {"a": "1", "b": "2"})
        assert url == "https://example.com?a=1&b=2"

    def test_append_with_existing_question(self):
        url = build_url("https://example.com?x=0", {"a": "1"})
        assert url == "https://example.com?x=0&a=1"


class TestRequest:
    def test_returns_parsed_json(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({"hello": "world"})
        result = request("https://example.com")
        assert result == {"hello": "world"}

    def test_returns_content_dict_for_plain_text(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response("plain text")
        result = request("https://example.com")
        assert result == {"content": "plain text"}

    def test_user_agent_added(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({})
        request("https://example.com")
        sent_headers = mock_urlopen.call_args.kwargs["headers"]
        assert sent_headers["User-Agent"] == "aa_agent_tools/0.1 (+https://github.com/Adullam-Technologies/aa_agent_tools)"

    def test_custom_headers_merged(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({})
        request("https://example.com", headers={"X-Token": "abc"})
        sent_headers = mock_urlopen.call_args.kwargs["headers"]
        assert sent_headers["X-Token"] == "abc"
        assert sent_headers["User-Agent"].startswith("aa_agent_tools/")

    def test_json_body_sets_content_type(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({})
        request("https://example.com", method="POST", json_body={"x": 1})
        sent_headers = mock_urlopen.call_args.kwargs["headers"]
        assert sent_headers["Content-Type"] == "application/json"
        assert json.loads(mock_urlopen.call_args.kwargs["body"]) == {"x": 1}

    def test_http_error_raises_request_error(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response("Not Found", status_code=404, reason="Not Found")
        from aa_agent_tools.errors import AARequestError

        with pytest.raises(AARequestError) as exc_info:
            request("https://example.com")
        assert exc_info.value.status == 404

    def test_url_error_raises_aa_error(self, mock_urlopen):
        import urllib3

        mock_urlopen.side_effect = urllib3.exceptions.MaxRetryError(None, "https://example.com", "refused")
        from aa_agent_tools.errors import AAError

        with pytest.raises(AAError, match="Could not reach"):
            request("https://example.com")

    def test_params_added_to_url(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({})
        request("https://example.com", params={"q": "hello"})
        sent_url = mock_urlopen.call_args.kwargs["url"]
        assert "q=hello" in sent_url

    def test_method_uppercased(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({})
        request("https://example.com", method="post")
        assert mock_urlopen.call_args.kwargs["method"] == "POST"

    def test_gzip_response_decompressed(self, mock_urlopen, fake_response):
        """Gzipped responses should be transparently decompressed by urllib3."""
        import gzip as gz

        raw_json = '{"hello": "world"}'
        gz_bytes = gz.compress(raw_json.encode("utf-8"))
        # ``fake_response`` accepts bytes and stores them in ``.data``; urllib3
        # would normally decompress, so simulate the already-decompressed body.
        mock_urlopen.return_value = fake_response(raw_json)
        # sanity check the gzip round-trip works
        assert gz.decompress(gz_bytes) == raw_json.encode("utf-8")
        result = request("https://example.com")
        assert result == {"hello": "world"}