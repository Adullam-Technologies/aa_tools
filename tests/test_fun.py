"""Tests for aa_tools.fun."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from aa_tools import fun


class TestRollDice:
    def test_default_range(self):
        for _ in range(100):
            result = fun.roll_dice()
            assert 1 <= result <= 6

    def test_custom_sides(self):
        for _ in range(100):
            result = fun.roll_dice(20)
            assert 1 <= result <= 20

    def test_minimum_two_sides(self):
        # max(2, sides) ensures at least 2
        result = fun.roll_dice(1)
        assert 1 <= result <= 2


class TestFlipCoin:
    def test_returns_valid_value(self):
        for _ in range(100):
            assert fun.flip_coin() in ("heads", "tails")


class TestRandomNumber:
    def test_default_range(self):
        for _ in range(100):
            result = fun.random_number()
            assert 1 <= result <= 100

    def test_custom_range(self):
        for _ in range(100):
            result = fun.random_number(10, 20)
            assert 10 <= result <= 20


class TestPickOne:
    def test_returns_one_of_items(self):
        items = ("a", "b", "c", "d")
        for _ in range(100):
            assert fun.pick_one(*items) in items

    def test_single_item(self):
        assert fun.pick_one("only") == "only"


class TestGetJoke:
    def test_success(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({"setup": "Why?", "punchline": "Because!"})
        result = fun.get_joke()
        assert result == {"setup": "Why?", "punchline": "Because!"}

    def test_failure_returns_fallback(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("network down")
        result = fun.get_joke()
        assert "setup" in result
        assert "punchline" in result
        assert len(result["setup"]) > 0


class TestGetCatFact:
    def test_success(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({"fact": "Cats purr."})
        assert fun.get_cat_fact() == "Cats purr."

    def test_failure_returns_fallback(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("nope")
        result = fun.get_cat_fact()
        assert isinstance(result, str)
        assert len(result) > 0


class TestGetDogImage:
    def test_success(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({"message": "https://dog.jpg"})
        assert fun.get_dog_image() == "https://dog.jpg"

    def test_failure_returns_fallback(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("nope")
        result = fun.get_dog_image()
        assert isinstance(result, str)
        assert result.startswith("http")


class TestGetCatImage:
    def test_returns_url(self):
        assert fun.get_cat_image() == "https://cataas.com/cat"


class TestGetQuote:
    def test_success(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({"content": "Be kind.", "author": "Me"})
        result = fun.get_quote()
        assert result == {"text": "Be kind.", "author": "Me"}

    def test_failure_returns_fallback(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("nope")
        result = fun.get_quote()
        assert result["text"]
        assert result["author"]


class TestGetAdvice:
    def test_success(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({"slip": {"advice": "Be happy."}})
        assert fun.get_advice() == "Be happy."

    def test_failure_returns_fallback(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("nope")
        result = fun.get_advice()
        assert isinstance(result, str)
        assert len(result) > 0


class TestGetPokemon:
    def test_success(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({
            "name": "pikachu",
            "types": [{"type": {"name": "electric"}}],
            "height": 4,
            "weight": 60,
            "sprites": {"front_default": "https://pikachu.png"},
        })
        result = fun.get_pokemon("pikachu")
        assert result["name"] == "pikachu"
        assert result["types"] == ["electric"]
        assert result["sprite"] == "https://pikachu.png"
        assert result["height"] == 4

    def test_name_lowercased(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({"name": "charizard", "types": [], "sprites": {}})
        fun.get_pokemon("Charizard")
        sent_url = mock_urlopen.call_args[0][0].full_url
        assert "charizard" in sent_url

    def test_failure_returns_fallback(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("nope")
        result = fun.get_pokemon("unknown")
        assert result["name"] == "unknown"
        assert result["types"] == []