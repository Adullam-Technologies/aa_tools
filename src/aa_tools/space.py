"""Space pictures and facts from NASA (no key needed for a few calls/day)."""

from __future__ import annotations

from ._http import request

NASA = "https://api.nasa.gov"


def space_image(date: str | None = None, *, api_key: str = "DEMO_KEY"):
    """Get NASA's Astronomy Picture of the Day.

    Parameters
    ----------
    date : str | None
        A date like ``"2024-01-01"`` (default: today).
    api_key : str
        NASA key (https://api.nasa.gov/). ``"DEMO_KEY"`` works for light use.

    Returns
    -------
    dict
        ``title``, ``date``, ``explanation``, ``url`` (image) and
        ``media_type``.

    Example
    -------
    >>> pic = aa.space_image()
    >>> print(pic["title"], pic["url"])
    """
    data = request(
        f"{NASA}/planetary/apod",
        params={"api_key": api_key, "date": date},
    )
    return {
        "title": data.get("title", ""),
        "date": data.get("date", ""),
        "explanation": data.get("explanation", ""),
        "url": data.get("url", ""),
        "media_type": data.get("media_type", ""),
    }


def near_earth_objects(api_key: str = "DEMO_KEY", *, start_date: str | None = None, end_date: str | None = None):
    """List asteroids flying near Earth in a date range (NASA NeoWs)."""
    params = {"api_key": api_key}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    data = request(f"{NASA}/neo/rest/v1/feed", params=params)
    return {
        "count": data.get("element_count"),
        "asteroids": list((data.get("near_earth_objects") or {}).values()),
    }
