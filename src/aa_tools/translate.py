"""Translate text between languages.

Uses the free MyMemory translation service by default (no key needed for small
amounts). Optionally use DeepL with a key for higher quality.
"""

from __future__ import annotations

from ._http import request
from ._util import require_key, truncate

MYMEMORY = "https://api.mymemory.translated.net/get"


def translate_text(text: str, to_lang: str, *, from_lang: str = "en", api_key: str | None = None):
    """Translate ``text`` into ``to_lang`` (language code like ``"fr"``, ``"es"``).

    Parameters
    ----------
    text : str
        The text to translate.
    to_lang : str
        Target language code, e.g. ``"fr"``, ``"de"``, ``"yo"``, ``"zh"``.
    from_lang : str
        Source language code (default ``"en"``). Use ``"auto"`` to guess.
    api_key : str | None
        Optional DeepL key. If given, DeepL is used instead of MyMemory.

    Returns
    -------
    str
        The translated text.

    Example
    -------
    >>> aa.translate_text("Hello, world!", to_lang="fr")
    'Bonjour, le monde !'
    """
    if api_key:
        return _translate_deepl(text, to_lang, from_lang, api_key)
    data = request(
        MYMEMORY,
        params={"q": text, "langpair": f"{from_lang}|{to_lang}"},
    )
    try:
        return data["responseData"]["translatedText"]
    except (KeyError, TypeError):
        return truncate(str(data), 400)


def _translate_deepl(text: str, to_lang: str, from_lang: str, key: str) -> str:
    require_key(key, "api_key")
    body = {
        "text": [text],
        "target_lang": to_lang.upper(),
    }
    if from_lang and from_lang != "auto":
        body["source_lang"] = from_lang.upper()
    data = request(
        "https://api-free.deepl.com/v2/translate",
        method="POST",
        json_body=body,
        headers={"Authorization": f"DeepL-Auth-Key {key}"},
    )
    try:
        return data["translations"][0]["text"]
    except (KeyError, IndexError, TypeError):
        return str(data)
