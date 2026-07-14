"""Tests for aa_agent_tools.data."""

from __future__ import annotations

import pytest

from aa_agent_tools import data
from aa_agent_tools.data import _is_prime


class TestIsPrime:
    @pytest.mark.parametrize("n", [2, 3, 5, 7, 11, 13, 17, 19, 23])
    def test_primes(self, n):
        assert _is_prime(n) is True

    @pytest.mark.parametrize("n", [0, 1, 4, 6, 8, 9, 10, 12, 15, 21])
    def test_not_primes(self, n):
        assert _is_prime(n) is False

    def test_negative(self):
        assert _is_prime(-7) is False


class TestNumberFact:
    def test_basic_fact(self):
        result = data.number_fact(7)
        assert "7" in result
        assert "digit" in result
        assert "odd" in result
        assert "prime" in result

    def test_even_number(self):
        result = data.number_fact(4)
        assert "even" in result
        assert "prime" not in result

    def test_perfect_square(self):
        result = data.number_fact(9)
        assert "perfect square" in result

    def test_digit_sum(self):
        result = data.number_fact(123)
        assert "6" in result  # 1+2+3=6

    def test_year_kind(self):
        result = data.number_fact(1066, kind="year")
        assert "AD" in result

    def test_negative_year(self):
        result = data.number_fact(-500, kind="year")
        assert "BC" in result

    def test_factor_of_million(self):
        result = data.number_fact(2)
        assert "factor of 1,000,000" in result

    def test_non_number(self):
        result = data.number_fact("abc")
        assert "number of some kind" in result

    def test_zero(self):
        result = data.number_fact(0)
        assert "0" in result


class TestWikipediaSummary:
    def test_success(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({
            "title": "Penguin",
            "extract": "Penguins are birds.",
            "content_urls": {"desktop": {"page": "https://en.wikipedia.org/wiki/Penguin"}},
            "thumbnail": {"source": "https://penguin.jpg"},
        })
        result = data.wikipedia_summary("Penguin")
        assert result["title"] == "Penguin"
        assert result["summary"] == "Penguins are birds."
        assert result["url"] == "https://en.wikipedia.org/wiki/Penguin"
        assert result["image"] == "https://penguin.jpg"

    def test_failure_returns_empty(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("nope")
        result = data.wikipedia_summary("Nonexistent")
        assert result == {"title": "Nonexistent", "summary": "", "url": "", "image": ""}

    def test_spaces_replaced_with_underscores(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({"title": "Black hole", "extract": ""})
        data.wikipedia_summary("Black hole")
        sent_url = mock_urlopen.call_args.kwargs["url"]
        assert "Black_hole" in sent_url


class TestDefineWord:
    def test_success(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response([
            {
                "phonetic": "/ˌsɛrənˈdɪpɪti/",
                "meanings": [
                    {
                        "partOfSpeech": "noun",
                        "definitions": [
                            {"definition": "A lucky find.", "example": "It was serendipity."},
                        ],
                    },
                ],
            },
        ])
        result = data.define_word("serendipity")
        assert result["word"] == "serendipity"
        assert result["phonetic"] == "/ˌsɛrənˈdɪpɪti/"
        assert len(result["definitions"]) == 1
        assert "(noun)" in result["definitions"][0]
        assert "lucky find" in result["definitions"][0]

    def test_failure_returns_empty(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("nope")
        result = data.define_word("xyz")
        assert result == {"word": "xyz", "phonetic": "", "definitions": []}

    def test_error_dict_returns_empty(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({"error": "not found"})
        result = data.define_word("zzz")
        assert result["definitions"] == []

    def test_word_lowercased_in_url(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response([])
        data.define_word("Hello")
        sent_url = mock_urlopen.call_args.kwargs["url"]
        assert "hello" in sent_url

    def test_definitions_capped_at_five(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response([
            {"meanings": [{"definitions": [{"definition": f"def {i}"} for i in range(10)]}]}
        ])
        result = data.define_word("word")
        assert len(result["definitions"]) <= 5


class TestCountryInfo:
    def test_delegates_to_wikipedia(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({
            "title": "Japan",
            "extract": "Japan is a country.",
            "content_urls": {"desktop": {"page": "https://en.wikipedia.org/wiki/Japan"}},
            "thumbnail": {"source": "https://japan.jpg"},
        })
        result = data.country_info("Japan")
        assert result["name"] == "Japan"
        assert result["summary"] == "Japan is a country."
        assert result["url"] == "https://en.wikipedia.org/wiki/Japan"


class TestConvertMoney:
    def test_success(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({"rates": {"EUR": 0.92}})
        result = data.convert_money(10, "USD", "EUR")
        assert result == round(10 * 0.92, 2)

    def test_missing_rate_returns_none(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({"rates": {}})
        assert data.convert_money(10, "USD", "XYZ") is None

    def test_currency_uppercased(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({"rates": {"EUR": 0.92}})
        data.convert_money(10, "usd", "eur")
        sent_url = mock_urlopen.call_args.kwargs["url"]
        assert "USD" in sent_url


class TestShortenUrl:
    def test_success(self, mock_urlopen, fake_response):
        mock_urlopen.return_value = fake_response({"shorturl": "https://is.gd/abc"})
        result = data.shorten_url("https://example.com/very/long")
        assert result == "https://is.gd/abc"

    def test_failure_returns_original(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("nope")
        result = data.shorten_url("https://example.com/long")
        assert result == "https://example.com/long"