"""Get the weather anywhere in the world (OpenWeatherMap)."""

from __future__ import annotations

from ._http import request
from ._util import require_key


def get_weather(city: str, api_key: str, *, units: str = "metric"):
    """Look up the current weather for a city.

    Parameters
    ----------
    city : str
        City name, e.g. ``"Lagos"`` or ``"Tokyo"``.
    api_key : str
        OpenWeatherMap API key (https://openweathermap.org/api).
    units : str
        ``"metric"`` (°C), ``"imperial"`` (°F) or ``"standard"`` (K).

    Returns
    -------
    dict
        Friendly keys: ``city``, ``description``, ``temp``, ``feels_like``,
        ``humidity``, ``wind``.

    Example
    -------
    >>> w = aa.get_weather("London", api_key="YOUR_KEY")
    >>> print(f"It is {w['temp']}°C and {w['description']} in {w['city']}")
    """
    require_key(api_key, "api_key")
    data = request(
        "https://api.openweathermap.org/data/2.5/weather",
        params={"q": city, "appid": api_key, "units": units},
    )
    main = data.get("main", {})
    wind = data.get("wind", {})
    weather = (data.get("weather") or [{}])[0]
    return {
        "city": data.get("name", city),
        "description": weather.get("description", ""),
        "temp": main.get("temp"),
        "feels_like": main.get("feels_like"),
        "humidity": main.get("humidity"),
        "wind": wind.get("speed"),
    }


def get_forecast(city: str, api_key: str, *, units: str = "metric", days: int = 3):
    """Get a short multi-day forecast for a city (OpenWeatherMap)."""
    require_key(api_key, "api_key")
    data = request(
        "https://api.openweathermap.org/data/2.5/forecast",
        params={"q": city, "appid": api_key, "units": units, "cnt": days * 8},
    )
    out = []
    for item in data.get("list", [])[: days * 8 : 8]:
        main = item.get("main", {})
        weather = (item.get("weather") or [{}])[0]
        out.append(
            {
                "datetime": item.get("dt_txt", ""),
                "temp": main.get("temp"),
                "description": weather.get("description", ""),
            }
        )
    return out
