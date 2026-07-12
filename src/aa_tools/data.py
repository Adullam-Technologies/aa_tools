"""Look up facts, words, and numbers from free public knowledge APIs."""

from __future__ import annotations

from ._http import request
from ._util import truncate


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def wikipedia_summary(title: str, *, sentences: int = 3):
    """Get a short, friendly summary of a Wikipedia topic.

    Parameters
    ----------
    title : str
        The topic, e.g. ``"Black hole"`` or ``"Turtle"``.
    sentences : int
        About how many sentences to include.

    Returns
    -------
    dict
        ``title``, ``summary``, ``url`` and ``image``.

    Example
    -------
    >>> info = aa.wikipedia_summary("Aurora")
    >>> print(info["summary"])
    """
    try:
        data = request(
            f"https://en.wikipedia.org/api/rest_v1/page/summary/{title.replace(' ', '_')}"
        )
    except Exception:
        return {"title": title, "summary": "", "url": "", "image": ""}
    return {
        "title": data.get("title", title),
        "summary": data.get("extract", ""),
        "url": (data.get("content_urls") or {}).get("desktop", {}).get("page", ""),
        "image": (data.get("thumbnail") or {}).get("source", ""),
    }


def define_word(word: str):
    """Get the dictionary definition and example sentence for a word.

    Example
    -------
    >>> d = aa.define_word("serendipity")
    >>> print(d["definitions"][0])
    """
    try:
        data = request(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word.lower()}")
    except Exception:
        return {"word": word, "phonetic": "", "definitions": []}
    if isinstance(data, dict):  # error response
        return {"word": word, "phonetic": "", "definitions": []}
    defs = []
    phonetic = ""
    for entry in data:
        phonetic = phonetic or entry.get("phonetic", "")
        for meaning in entry.get("meanings", []):
            for d in meaning.get("definitions", []):
                defs.append(
                    f"({meaning.get('partOfSpeech', '')}) {d.get('definition', '')}"
                    + (f" e.g. {d['example']}" if d.get("example") else "")
                )
    return {"word": word, "phonetic": phonetic, "definitions": defs[:5]}


def number_fact(number, *, kind: str = "math"):
    """Get a fun, fact-packed description of a number (works offline!).

    The fact is computed for you, so it never needs the internet. Try
    ``kind="math"`` for number properties, or ``kind="year"`` / ``kind="date"``
    for a playful note.

    Example
    -------
    >>> aa.number_fact(7)
    '7 has 1 digit(s). Its digits add up to 7. 7 is odd. 7 is a prime number ...'
    """
    try:
        n = int(number)
    except (TypeError, ValueError):
        return f"{number} is... a number of some kind!"
    facts = [f"{n} has {len(str(abs(n)))} digit(s)."]
    digit_sum = sum(int(c) for c in str(abs(n)))
    facts.append(f"Its digits add up to {digit_sum}.")
    facts.append(f"{n} is {'even' if n % 2 == 0 else 'odd'}.")
    if _is_prime(abs(n)):
        facts.append(f"{n} is a prime number - only divisible by 1 and itself!")
    root = int(abs(n) ** 0.5)
    if root * root == abs(n) and n >= 0:
        facts.append(f"{n} is a perfect square ({root} × {root}).")
    if n != 0 and 1_000_000 % n == 0:
        facts.append(f"{n} is a factor of 1,000,000.")
    tail = {
        "year": f" If {n} were a year, it would be in the {'BC' if n < 0 else 'AD'} era.",
        "date": f" The {n}th day of the year is a special one!",
        "trivia": "",
        "math": "",
    }.get(kind, "")
    return " ".join(facts) + tail


def country_info(name: str):
    """Get a friendly snapshot of a country using Wikipedia.

    Example
    -------
    >>> c = aa.country_info("Japan")
    >>> print(c["name"]); print(c["summary"][:80])
    """
    info = wikipedia_summary(name)
    return {
        "name": info.get("title") or name,
        "summary": info.get("summary", ""),
        "url": info.get("url", ""),
        "image": info.get("image", ""),
    }


def convert_money(amount: float, from_currency: str, to_currency: str):
    """Convert money between currencies using live rates (no key needed).

    Example
    -------
    >>> aa.convert_money(10, "USD", "EUR")
    """
    from ._util import require_key

    data = request("https://open.er-api.com/v6/latest/" + from_currency.upper())
    rates = data.get("rates", {})
    rate = rates.get(to_currency.upper())
    if rate is None:
        return None
    return round(amount * float(rate), 2)


def shorten_url(url: str):
    """Make a long URL short using the free is.gd service."""
    try:
        data = request("https://is.gd/create.php", params={"format": "json", "url": url})
        if isinstance(data, dict):
            return data.get("shorturl", url)
    except Exception:
        pass
    return url
