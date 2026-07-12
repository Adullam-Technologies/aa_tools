"""Silly, fun, and delightful functions to surprise your agent (and you!)."""

from __future__ import annotations

import random

from ._http import request


def get_joke():
    """Get a random clean joke with a setup and punchline.

    Example
    -------
    >>> j = aa.get_joke()
    >>> print(j["setup"]); print(j["punchline"])
    """
    try:
        data = request("https://official-joke-api.appspot.com/random_joke")
        return {"setup": data.get("setup", ""), "punchline": data.get("punchline", "")}
    except Exception:
        return {"setup": "Why did the computer go to school?", "punchline": "To improve its byte!"}


def get_cat_fact():
    """Get a random fact about cats."""
    try:
        return request("https://catfact.ninja/fact").get("fact", "")
    except Exception:
        return "Cats spend about 70% of their lives sleeping."


def get_dog_image():
    """Get a random photo of a good dog."""
    try:
        return request("https://dog.ceo/api/breeds/image/random").get("message", "")
    except Exception:
        return "https://images.dog.ceo/breeds/pug/n02110958_13952.jpg"


def get_cat_image():
    """Get a random photo of a cat."""
    return "https://cataas.com/cat"


def get_quote():
    """Get an inspirational quote (text + who said it)."""
    try:
        data = request("https://api.quotable.io/random")
        return {"text": data.get("content", ""), "author": data.get("author", "")}
    except Exception:
        return {
            "text": "The best way to predict the future is to invent it.",
            "author": "Alan Kay",
        }


def get_advice():
    """Get a random piece of (silly but wise) advice.

    Example
    -------
    >>> aa.get_advice()
    'Always carry a spare rubber band.'
    """
    try:
        data = request("https://api.adviceslip.com/advice")
        return data.get("slip", {}).get("advice", "")
    except Exception:
        return "When in doubt, take a deep breath and try again."


def roll_dice(sides: int = 6):
    """Roll a die with ``sides`` faces (default 6)."""
    return random.randint(1, max(2, sides))


def flip_coin():
    """Flip a coin. Returns ``"heads"`` or ``"tails"``."""
    return random.choice(["heads", "tails"])


def random_number(min_value: int = 1, max_value: int = 100):
    """Pick a random whole number between ``min_value`` and ``max_value``."""
    return random.randint(min_value, max_value)


def pick_one(*items):
    """Randomly choose one item from the list you provide."""
    return random.choice(list(items))


def get_pokemon(name: str = "pikachu"):
    """Look up a Pokémon by name (or id). Returns its type, height, and a picture.

    Example
    -------
    >>> p = aa.get_pokemon("charizard")
    >>> print(p["name"], p["types"], p["sprite"])
    """
    try:
        data = request(f"https://pokeapi.co/api/v2/pokemon/{name.lower()}")
        return {
            "name": data.get("name"),
            "types": [t["type"]["name"] for t in data.get("types", [])],
            "height": data.get("height"),
            "weight": data.get("weight"),
            "sprite": (data.get("sprites") or {}).get("front_default"),
        }
    except Exception:
        return {"name": name, "types": [], "height": None, "weight": None, "sprite": None}
