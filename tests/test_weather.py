"""Tests for aa_tools.weather."""

from __future__ import annotations

import pytest

from aa_tools import weather
from aa_tools.errors import AAMissingKeyError


SAMPLE_OWM_RESPONSE = {
    "name": "London",
    "main": {"temp": 15.5, "feels_like": 14.0, "humidity": 80},
    "wind": {"speed": 3.5},
    "weather": [{"description": "broken clouds"}],
}


class TestGetWeather:
    def test_requires_api_key(self):
        with pytest.raises(AAMissingKeyError):
            weather.get_weather("London", "")

    def test_success(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response(SAMPLE_OWM_RESPONSE)
        result = weather.get_weather("London", "key")
        assert result["city"] == "London"
        assert result["temp"] == 15.5
        assert result["feels_like"] == 14.0
        assert result["humidity"] == 80
        assert result["wind"] == 3.5
        assert result["description"] == "broken clouds"

    def test_sends_units_param(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response(SAMPLE_OWM_RESPONSE)
        weather.get_weather("London", "key", units="imperial")
        sent_url = mock_urlopen.call_args[0][0].full_url
        assert "units=imperial" in sent_url

    def test_sends_city_in_query(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response(SAMPLE_OWM_RESPONSE)
        weather.get_weather("Tokyo", "key")
        sent_url = mock_urlopen.call_args[0][0].full_url
        assert "q=Tokyo" in sent_url

    def test_missing_weather_key_defaults(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({"name": "X", "main": {}, "wind": {}})
        result = weather.get_weather("X", "key")
        assert result["description"] == ""
        assert result["temp"] is None


class TestGetForecast:
    def test_requires_api_key(self):
        with pytest.raises(AAMissingKeyError):
            weather.get_forecast("London", "")

    def test_returns_forecast_list(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({
            "list": [
                {"dt_txt": "2024-01-01 12:00", "main": {"temp": 10}, "weather": [{"description": "sunny"}]},
                {"dt_txt": "2024-01-02 12:00", "main": {"temp": 12}, "weather": [{"description": "rain"}]},
                {"dt_txt": "2024-01-03 12:00", "main": {"temp": 8}, "weather": [{"description": "cloudy"}]},
            ]
        })
        result = weather.get_forecast("London", "key", days=3)
        assert len(result) <= 3
        assert result[0]["temp"] == 10
        assert result[0]["description"] == "sunny"