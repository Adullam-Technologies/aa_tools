"""Tests for aa_agent_tools.space."""

from __future__ import annotations

import pytest

from aa_agent_tools import space


SAMPLE_APOD = {
    "title": "Andromeda Galaxy",
    "date": "2024-01-01",
    "explanation": "A nearby spiral galaxy.",
    "url": "https://apod.nasa.gov/apod/image/2401/andromeda.jpg",
    "media_type": "image",
}


class TestSpaceImage:
    def test_success(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response(SAMPLE_APOD)
        result = space.space_image()
        assert result["title"] == "Andromeda Galaxy"
        assert result["date"] == "2024-01-01"
        assert result["explanation"] == "A nearby spiral galaxy."
        assert result["url"] == "https://apod.nasa.gov/apod/image/2401/andromeda.jpg"
        assert result["media_type"] == "image"

    def test_api_key_sent(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response(SAMPLE_APOD)
        space.space_image(api_key="MYKEY")
        sent_url = mock_urlopen.call_args[0][0].full_url
        assert "api_key=MYKEY" in sent_url

    def test_demo_key_by_default(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response(SAMPLE_APOD)
        space.space_image()
        sent_url = mock_urlopen.call_args[0][0].full_url
        assert "api_key=DEMO_KEY" in sent_url

    def test_date_param(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response(SAMPLE_APOD)
        space.space_image("2024-06-15")
        sent_url = mock_urlopen.call_args[0][0].full_url
        assert "date=2024-06-15" in sent_url


class TestNearEarthObjects:
    def test_success(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({
            "element_count": 3,
            "near_earth_objects": {
                "2024-01-01": [{"name": "Asteroid 1"}],
                "2024-01-02": [{"name": "Asteroid 2"}],
            },
        })
        result = space.near_earth_objects()
        assert result["count"] == 3
        assert len(result["asteroids"]) == 2

    def test_empty(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({})
        result = space.near_earth_objects()
        assert result["count"] is None
        assert result["asteroids"] == []

    def test_date_params(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({})
        space.near_earth_objects(start_date="2024-01-01", end_date="2024-01-07")
        sent_url = mock_urlopen.call_args[0][0].full_url
        assert "start_date=2024-01-01" in sent_url
        assert "end_date=2024-01-07" in sent_url