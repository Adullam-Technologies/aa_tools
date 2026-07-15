"""Tests for aa_agent_tools._util."""

from __future__ import annotations

import pytest

from aa_agent_tools._util import pretty, require_key
from aa_agent_tools.errors import AAMissingKeyError


class TestRequireKey:
    def test_returns_value_when_truthy(self):
        assert require_key("secret", "api_key") == "secret"

    def test_raises_when_empty_string(self):
        with pytest.raises(AAMissingKeyError) as exc:
            require_key("", "api_key")
        assert exc.value.key_name == "api_key"

    def test_raises_when_none(self):
        with pytest.raises(AAMissingKeyError):
            require_key(None, "token")

    def test_raises_when_zero(self):
        # 0 is falsy → should raise
        with pytest.raises(AAMissingKeyError):
            require_key(0, "key")

    def test_error_message_contains_name(self):
        with pytest.raises(AAMissingKeyError, match="api_key"):
            require_key("", "api_key")


class TestPretty:
    def test_dict_pretty_printed(self):
        result = pretty({"b": 2, "a": 1})
        assert '"a"' in result
        assert '"b"' in result
        assert "\n" in result

    def test_list_pretty_printed(self):
        result = pretty([1, 2, 3])
        assert "1" in result
        assert "\n" in result

    def test_string_passthrough(self):
        assert pretty("hello") == "hello"

    def test_int_passthrough(self):
        assert pretty(42) == "42"