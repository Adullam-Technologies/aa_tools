"""Tests for aa_tools.text_tools."""

from __future__ import annotations

import base64 as b64
import hashlib
import urllib.parse

import pytest

from aa_tools.text_tools import (
    base64_decode,
    base64_encode,
    convert_units,
    count_words,
    hash_text,
    is_palindrome,
    make_qr,
    reverse_text,
)


class TestHashText:
    def test_sha256_default(self):
        result = hash_text("hello")
        expected = hashlib.sha256("hello".encode()).hexdigest()
        assert result == expected

    def test_md5(self):
        result = hash_text("hello", algorithm="md5")
        expected = hashlib.md5("hello".encode()).hexdigest()
        assert result == expected

    def test_empty_string(self):
        result = hash_text("")
        expected = hashlib.sha256(b"").hexdigest()
        assert result == expected


class TestBase64:
    def test_encode(self):
        assert base64_encode("hello") == b64.b64encode(b"hello").decode()

    def test_decode(self):
        encoded = base64_encode("world")
        assert base64_decode(encoded) == "world"

    def test_roundtrip_unicode(self):
        encoded = base64_encode("héllo wörld")
        assert base64_decode(encoded) == "héllo wörld"


class TestMakeQr:
    def test_default_size(self):
        url = make_qr("test")
        assert "size=200x200" in url
        assert f"data={urllib.parse.quote('test')}" in url

    def test_custom_size(self):
        url = make_qr("abc", size=300)
        assert "size=300x300" in url

    def test_url_encoded(self):
        url = make_qr("https://example.com?q=1&x=2")
        assert urllib.parse.quote("https://example.com?q=1&x=2") in url


class TestConvertUnits:
    def test_length_km_to_m(self):
        assert convert_units(1, "km", "m") == 1000.0

    def test_length_mi_to_km(self):
        result = convert_units(1, "mi", "km")
        assert abs(result - 1.60934) < 0.001

    def test_weight_kg_to_lb(self):
        result = convert_units(1, "kg", "lb")
        assert abs(result - 2.20462) < 0.001

    def test_same_unit(self):
        assert convert_units(5, "m", "m") == 5.0

    def test_case_insensitive(self):
        assert convert_units(1, "KM", "M") == 1000.0

    def test_cross_dimension_raises(self):
        with pytest.raises(ValueError, match="Cannot convert"):
            convert_units(1, "kg", "m")

    def test_unknown_unit_raises(self):
        with pytest.raises(ValueError, match="Cannot convert"):
            convert_units(1, "foo", "bar")


class TestCountWords:
    def test_simple(self):
        assert count_words("hello world") == 2

    def test_single(self):
        assert count_words("hello") == 1

    def test_empty(self):
        assert count_words("") == 0

    def test_extra_whitespace(self):
        assert count_words("  hello   world  ") == 2


class TestReverseText:
    def test_simple(self):
        assert reverse_text("hello") == "olleh"

    def test_palindrome(self):
        assert reverse_text("racecar") == "racecar"

    def test_empty(self):
        assert reverse_text("") == ""


class TestIsPalindrome:
    @pytest.mark.parametrize("text", ["racecar", "madam", "A man a plan a canal Panama", "No 'x' in Nixon"])
    def test_palindromes(self, text):
        assert is_palindrome(text) is True

    @pytest.mark.parametrize("text", ["hello", "world", "python"])
    def test_not_palindromes(self, text):
        assert is_palindrome(text) is False

    def test_empty_string(self):
        assert is_palindrome("") is True

    def test_case_insensitive(self):
        assert is_palindrome("RaceCar") is True