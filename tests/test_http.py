"""Tests for aa_tools._http."""

from __future__ import annotations

import json
import urllib.error

import pytest

from aa_tools._http import build_url, request


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
        sent_req = mock_urlopen.call_args[0][0]
        assert sent_req.headers["User-agent"] == "aa_tools/0.1 (+https://github.com/Adullam-Technologies/aa_tools)"

    def test_custom_headers_merged(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({})
        request("https://example.com", headers={"X-Token": "abc"})
        sent_req = mock_urlopen.call_args[0][0]
        assert sent_req.headers["X-token"] == "abc"
        assert sent_req.headers["User-agent"].startswith("aa_tools/")

    def test_json_body_sets_content_type(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({})
        request("https://example.com", method="POST", json_body={"x": 1})
        sent_req = mock_urlopen.call_args[0][0]
        assert sent_req.headers["Content-type"] == "application/json"
        assert json.loads(sent_req.data) == {"x": 1}

    def test_http_error_raises_request_error(self, mock_urlopen):
        err = urllib.error.HTTPError(
            "https://example.com", 404, "Not Found", {}, None
        )
        mock_urlopen.side_effect = err
        from aa_tools.errors import AARequestError

        with pytest.raises(AARequestError) as exc_info:
            request("https://example.com")
        assert exc_info.value.status == 404

    def test_url_error_raises_aa_error(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.URLError("refused")
        from aa_tools.errors import AAError

        with pytest.raises(AAError, match="Could not reach"):
            request("https://example.com")

    def test_params_added_to_url(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({})
        request("https://example.com", params={"q": "hello"})
        sent_req = mock_urlopen.call_args[0][0]
        assert "q=hello" in sent_req.full_url

    def test_method_uppercased(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({})
        request("https://example.com", method="post")
        sent_req = mock_urlopen.call_args[0][0]
        assert sent_req.method == "POST"

    def test_gzip_response_decompressed(self, mock_urlopen):
        """Gzipped responses should be transparently decompressed."""
        import gzip as gz

        raw_json = '{"hello": "world"}'
        gz_bytes = gz.compress(raw_json.encode("utf-8"))

        class _GzipResponse:
            headers = {"Content-Encoding": "gzip"}

            def __enter__(self):
                return self

            def __exit__(self, *exc):
                return False

            def read(self):
                return gz_bytes

        mock_urlopen.return_value = _GzipResponse()
        result = request("https://example.com")
        assert result == {"hello": "world"}