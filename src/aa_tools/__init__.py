"""aa_tools - a friendly toolbox of cool functions for kid-built agents.

Import it and call functions directly::

    import aa_tools as aa

    aa.search_web("cute penguins", api_key="YOUR_BRAVE_KEY")
    aa.fetch_page("https://example.com")
    aa.get_joke()
    aa.ask_ai("What is recursion?", api_key="YOUR_OPENAI_KEY")

Every function that needs a secret (an API key, a password, ...) takes it as
an argument. We never store your keys.
"""

from __future__ import annotations

__version__ = "0.1.0"

# ---- re-export the friendly public functions -----------------------------
from .apis import call_api
from .data import (
    convert_money,
    country_info,
    define_word,
    number_fact,
    shorten_url,
    wikipedia_summary,
)
from .email_tools import send_email, send_email_gmail
from .errors import AAError, AARequestError
from .fun import (
    flip_coin,
    get_advice,
    get_cat_fact,
    get_cat_image,
    get_dog_image,
    get_joke,
    get_pokemon,
    get_quote,
    pick_one,
    random_number,
    roll_dice,
)
from .images import get_photo, random_image
from .space import near_earth_objects, space_image
from .text_tools import (
    base64_decode,
    base64_encode,
    convert_units,
    count_words,
    hash_text,
    is_palindrome,
    make_qr,
    reverse_text,
)
from .weather import get_forecast, get_weather
from .web import fetch_page, search_web

__all__ = [
    # web
    "search_web",
    "fetch_page",
    # email
    "send_email",
    "send_email_gmail",
    # generic api + ai
    "call_api",
    # weather
    "get_weather",
    "get_forecast",
    # space
    "space_image",
    "near_earth_objects",
    # fun
    "get_joke",
    "get_advice",
    "get_cat_fact",
    "get_cat_image",
    "get_dog_image",
    "get_quote",
    "roll_dice",
    "flip_coin",
    "random_number",
    "pick_one",
    "get_pokemon",
    # data / knowledge
    "wikipedia_summary",
    "define_word",
    "number_fact",
    "country_info",
    "convert_money",
    "shorten_url",
    # images
    "get_photo",
    "random_image",
    # text tools
    "hash_text",
    "base64_encode",
    "base64_decode",
    "make_qr",
    "convert_units",
    "count_words",
    "reverse_text",
    "is_palindrome",
    # errors
    "AAError",
    "AARequestError",
]


def list_functions() -> list[str]:
    """Return the names of every function in aa_tools (handy for autocomplete)."""
    return list(__all__)


def about() -> str:
    """Print a friendly welcome message."""
    return (
        "aa_tools v"
        + __version__
        + " - a friendly toolbox of cool functions for kid-built agents.\n"
        "Try: aa.search_web(...), aa.fetch_page(...), aa.get_joke(), aa.ask_ai(...)\n"
        "Need a key? Pass it as an argument - we never store your secrets."
    )
