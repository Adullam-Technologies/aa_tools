"""Tests for aa_tools.apis."""

from __future__ import annotations

import json

import pytest

from aa_tools import apis
from aa_tools.errors import AAMissingKeyError


class TestCallApi:
    def test_get_request(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({"result": "ok"})
        result = apis.call_api("https://api.example.com/data")
        assert result == {"result": "ok"}

    def test_no_key_no_auth_header(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({})
        apis.call_api("https://api.example.com")
        sent_req = mock_urlopen.call_args[0][0]
        assert "Authorization" not in sent_req.headers

    def test_key_added_to_header(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({})
        apis.call_api("https://api.example.com", api_key="secret")
        sent_req = mock_urlopen.call_args[0][0]
        assert sent_req.headers["Authorization"] == "Bearer secret"

    def test_custom_key_header_and_prefix(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({})
        apis.call_api("https://api.example.com", api_key="tok", key_header="X-Api-Key", key_prefix="")
        sent_req = mock_urlopen.call_args[0][0]
        assert sent_req.headers["X-api-key"] == "tok"

    def test_post_with_json_body(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({"created": True})
        result = apis.call_api("https://api.example.com", method="POST", json_body={"x": 1})
        assert result == {"created": True}
        sent_req = mock_urlopen.call_args[0][0]
        assert sent_req.method == "POST"
        assert json.loads(sent_req.data) == {"x": 1}

    def test_params_sent(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({})
        apis.call_api("https://api.example.com", params={"q": "test"})
        sent_req = mock_urlopen.call_args[0][0]
        assert "q=test" in sent_req.full_url

    def test_extra_headers_merged(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({})
        apis.call_api("https://api.example.com", extra_headers={"X-Custom": "val"})
        sent_req = mock_urlopen.call_args[0][0]
        assert sent_req.headers["X-custom"] == "val"