"""Tests for aa_agent_tools.errors."""

from __future__ import annotations

import pytest

from aa_agent_tools.errors import AAError, AARequestError, AAMissingKeyError


class TestAAError:
    def test_is_exception(self):
        assert issubclass(AAError, Exception)

    def test_can_raise_and_catch(self):
        with pytest.raises(AAError, match="boom"):
            raise AAError("boom")


class TestAARequestError:
    def test_is_aa_error(self):
        assert issubclass(AARequestError, AAError)

    def test_attributes_stored(self):
        err = AARequestError(404, "Not Found", "nope")
        assert err.status == 404
        assert err.reason == "Not Found"
        assert err.body == "nope"

    @pytest.mark.parametrize(
        "status,expected_hint",
        [
            (401, "did you forget your API key"),
            (403, "this key is not allowed"),
            (404, "nothing was found"),
            (429, "rate limit"),
            (500, ""),  # no hint for 500
        ],
    )
    def test_hints(self, status, expected_hint):
        err = AARequestError(status, "Reason")
        if expected_hint:
            assert expected_hint in str(err)
        else:
            assert str(err) == f"HTTP {status} Reason"

    def test_caught_as_aa_error(self):
        with pytest.raises(AAError):
            raise AARequestError(400, "Bad Request")


class TestAAMissingKeyError:
    def test_is_aa_error(self):
        assert issubclass(AAMissingKeyError, AAError)

    def test_key_name_stored(self):
        err = AAMissingKeyError("api_key")
        assert err.key_name == "api_key"
        assert "api_key" in str(err)
        assert "YOUR_KEY" in str(err)