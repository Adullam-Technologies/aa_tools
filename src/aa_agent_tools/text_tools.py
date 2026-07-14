"""Handy text + utility helpers that need no internet (except QR images)."""

from __future__ import annotations

import base64
import hashlib
import urllib.parse

from ._http import request


def hash_text(text: str, *, algorithm: str = "sha256"):
    """Turn text into a fixed "fingerprint" hash.

    Example
    -------
    >>> aa.hash_text("hello")
    '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
    """
    h = hashlib.new(algorithm)
    h.update(text.encode("utf-8"))
    return h.hexdigest()


def base64_encode(text: str):
    """Encode text into Base64 (a common way to pack data)."""
    return base64.b64encode(text.encode("utf-8")).decode("ascii")


def base64_decode(text: str):
    """Decode Base64 text back to normal text."""
    return base64.b64decode(text.encode("ascii")).decode("utf-8", errors="replace")


def make_qr(text: str, *, size: int = 200):
    """Make a QR code image for ``text`` and return its URL.

    Example
    -------
    >>> aa.make_qr("https://example.com")
    'https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=...'
    """
    return (
        "https://api.qrserver.com/v1/create-qr-code/"
        f"?size={size}x{size}&data={urllib.parse.quote(text)}"
    )


# ---- tiny unit converter -------------------------------------------------
_LENGTH = {"m": 1.0, "km": 1000.0, "cm": 0.01, "mm": 0.001, "mi": 1609.34, "yd": 0.9144, "ft": 0.3048, "in": 0.0254}
_WEIGHT = {"kg": 1.0, "g": 0.001, "mg": 1e-6, "lb": 0.453592, "oz": 0.0283495}


def convert_units(value: float, from_unit: str, to_unit: str):
    """Convert between length or weight units.

    Example
    -------
    >>> aa.convert_units(1, "mi", "km")   # ~1.609
    >>> aa.convert_units(1, "kg", "lb")   # ~2.205
    """
    f, t = from_unit.lower(), to_unit.lower()
    if f in _LENGTH and t in _LENGTH:
        return round(value * _LENGTH[f] / _LENGTH[t], 6)
    if f in _WEIGHT and t in _WEIGHT:
        return round(value * _WEIGHT[f] / _WEIGHT[t], 6)
    raise ValueError(f"Cannot convert '{from_unit}' to '{to_unit}'. Try length (m,km,cm,mm,mi,yd,ft,in) or weight (kg,g,mg,lb,oz).")


def count_words(text: str) -> int:
    """Count the words in some text."""
    return len(text.split())


def reverse_text(text: str) -> str:
    """Reverse a string."""
    return text[::-1]


def is_palindrome(text: str) -> bool:
    """Is the text the same forwards and backwards (ignoring spaces/case)?"""
    cleaned = "".join(ch.lower() for ch in text if ch.isalnum())
    return cleaned == cleaned[::-1]
