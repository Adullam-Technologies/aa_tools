"""Tests for aa_agent_tools.images."""

from __future__ import annotations

import pytest

from aa_agent_tools import images
from aa_agent_tools.errors import AAMissingKeyError


class TestGetPhoto:
    def test_requires_key(self):
        with pytest.raises(AAMissingKeyError):
            images.get_photo("cats", "")

    def test_success(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({
            "photos": [
                {"src": {"large": "https://p1.jpg"}},
                {"src": {"large": "https://p2.jpg"}},
            ]
        })
        result = images.get_photo("cats", "key")
        assert result == ["https://p1.jpg", "https://p2.jpg"]

    def test_empty(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({})
        assert images.get_photo("x", "key") == []

    def test_auth_header(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({"photos": []})
        images.get_photo("cats", "pexelskey")
        sent_req = mock_urlopen.call_args[0][0]
        assert sent_req.headers["Authorization"] == "pexelskey"

    def test_count_param(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({"photos": []})
        images.get_photo("cats", "key", count=5)
        sent_url = mock_urlopen.call_args[0][0].full_url
        assert "per_page=5" in sent_url


class TestRandomImage:
    def test_default_dimensions(self):
        url = images.random_image()
        assert url == "https://picsum.photos/400/300"

    def test_custom_dimensions(self):
        url = images.random_image(width=800, height=600)
        assert url == "https://picsum.photos/800/600"

    def test_with_seed(self):
        url = images.random_image(seed="abc")
        assert url == "https://picsum.photos/seed/abc/400/300"

    def test_with_seed_and_dimensions(self):
        url = images.random_image(width=100, height=200, seed="xyz")
        assert url == "https://picsum.photos/seed/xyz/100/200"