"""Make and grab pictures - AI-generated art and free stock photos."""

from __future__ import annotations

from ._http import request
from ._util import require_key


def get_photo(query: str, api_key: str, *, count: int = 1):
    """Search free stock photos on Pexels and return image URLs.

    Get a free key at https://www.pexels.com/api/.
    """
    require_key(api_key, "api_key")
    data = request(
        "https://api.pexels.com/v1/search",
        params={"query": query, "per_page": max(1, count)},
        headers={"Authorization": api_key},
    )
    return [p.get("src", {}).get("large") or p.get("url") for p in data.get("photos", [])]


def random_image(*, width: int = 400, height: int = 300, seed: str | None = None):
    """Get a random photo of the given size (no key needed)."""
    if seed:
        return f"https://picsum.photos/seed/{seed}/{width}/{height}"
    return f"https://picsum.photos/{width}/{height}"
