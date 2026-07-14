"""Live tests for aa_tools.weather (OpenWeatherMap).

These make real network calls and need an OpenWeatherMap API key. Run with::

    uv run pytest --live -m live tests/test_weather_live.py
"""

from __future__ import annotations

import pytest

from aa_tools import weather


pytestmark = pytest.mark.live


class TestGetWeatherLive:
    def test_get_weather_for_city(self, openweather_api_key):
        if not openweather_api_key:
            pytest.skip("OPEN_WEATHER_API_KEY not set")
        result = weather.get_weather("London", openweather_api_key)
        assert isinstance(result, dict)
        assert result["city"]  # should not be empty
        assert result["temp"] is not None
        assert isinstance(result["temp"], (int, float))
        assert result["description"]  # usually non-empty
        assert result["humidity"] is not None

    def test_get_weather_imperial_units(self, openweather_api_key):
        if not openweather_api_key:
            pytest.skip("OPEN_WEATHER_API_KEY not set")
        result = weather.get_weather("Lagos", openweather_api_key, units="imperial")
        assert result["temp"] is not None
        # imperial temps are in °F, typically > 30 for Lagos
        assert isinstance(result["temp"], (int, float))


class TestGetForecastLive:
    def test_get_forecast_returns_list(self, openweather_api_key):
        if not openweather_api_key:
            pytest.skip("OPEN_WEATHER_API_KEY not set")
        result = weather.get_forecast("London", openweather_api_key, days=3)
        assert isinstance(result, list)
        assert len(result) >= 1
        for entry in result:
            assert "datetime" in entry
            assert "temp" in entry
            assert "description" in entry