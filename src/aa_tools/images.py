"""Make and grab pictures - AI-generated art and free stock photos."""

from __future__ import annotations

from ._http import request
from ._util import require_key


def generate_image(prompt: str, api_key: str, *, size: str = "1024x1024", model: str = "dall-e-3"):
    """Create an image from a text description using OpenAI DALL·E.

    Parameters
    ----------
    prompt : str
        What you want the picture to show.
    api_key : str
        Your OpenAI API key.
    size : str
        One of ``"1024x1024"``, ``"1792x1024"`` or ``"1024x1792"``.
    model : str
        ``"dall-e-3"`` (default) or ``"dall-e-2"``.

    Returns
    -------
    str
        A URL to the generated image.

    Example
    -------
    >>> url = aa.generate_image("a robot riding a unicorn on the moon", api_key="YOUR_KEY")
    >>> print(url)
    """
    require_key(api_key, "api_key")
    body = {"prompt": prompt, "model": model, "n": 1, "size": size}
    data = request(
        "https://api.openai.com/v1/images/generations",
        method="POST",
        json_body=body,
        headers={"Authorization": f"Bearer {api_key}"},
    )
    try:
        item = data["data"][0]
        return item.get("url") or item.get("b64_json")
    except (KeyError, IndexError, TypeError):
        return str(data)


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
