"""Shared fixtures and helpers for the aa_tools test-suite.

Offline (mocked) tests run by default.  Live tests that hit real APIs are
opt-in: they only run when the relevant key is present in a ``.env`` file (or
already in the environment) **and** the ``--live`` flag is passed to pytest.

Usage
-------
    uv run pytest                # offline only (default, CI-friendly)
    uv run pytest --live         # include live tests when keys are available
    uv run pytest --live -m live # live tests only
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from unittest.mock import patch

import pytest


# ---------------------------------------------------------------------------
# .env loading (no third-party dependency required)
# ---------------------------------------------------------------------------

def _load_dotenv(path: Path) -> None:
    """Populate ``os.environ`` from a simple ``KEY=VALUE`` .env file."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip()
        # strip surrounding quotes
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]
        os.environ.setdefault(key, value)


_load_dotenv(Path(__file__).resolve().parent.parent / ".env")


# ---------------------------------------------------------------------------
# pytest flag: --live
# ---------------------------------------------------------------------------

def pytest_addoption(parser):
    parser.addoption(
        "--live",
        action="store_true",
        default=False,
        help="Enable live tests that hit real external APIs.",
    )


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "live: tests that make real network calls (run with --live)",
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--live"):
        return
    skip_live = pytest.mark.skip(reason="needs --live flag and real API keys")
    for item in items:
        if "live" in item.keywords:
            item.add_marker(skip_live)


# ---------------------------------------------------------------------------
# Helpers for reading keys from the environment
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def brave_api_key() -> str:
    return os.environ.get("BRAVE_API_KEY", "")


@pytest.fixture(scope="session")
def openweather_api_key() -> str:
    return os.environ.get("OPEN_WEATHER_API_KEY", "")


@pytest.fixture(scope="session")
def gmail_address() -> str:
    return os.environ.get("GMAIL_ADDRESS", "")


@pytest.fixture(scope="session")
def gmail_app_password() -> str:
    return os.environ.get("GMAIL_APP_PASSWORD", "")


@pytest.fixture(scope="session")
def email_to() -> str:
    return os.environ.get("TO", "")


# ---------------------------------------------------------------------------
# A fake ``urlopen`` context manager that mimics urllib.request.urlopen
# ---------------------------------------------------------------------------

class _FakeResponse:
    """Minimal stand-in for the object returned by ``urllib.request.urlopen``."""

    def __init__(self, payload, *, status_code: int = 200, headers=None):
        if isinstance(payload, (dict, list)):
            self._raw = json.dumps(payload).encode("utf-8")
        elif isinstance(payload, str):
            self._raw = payload.encode("utf-8")
        else:
            self._raw = payload or b""
        self.status_code = status_code
        self.headers = headers or {}

    # context-manager protocol
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def read(self) -> bytes:
        return self._raw

    # some helpers that the real response has
    def getcode(self) -> int:
        return self.status_code

    def info(self):
        return self.headers


def make_response(payload, *, status_code: int = 200, headers=None) -> _FakeResponse:
    """Return a :class:`_FakeResponse` object."""
    return _FakeResponse(payload, status_code=status_code, headers=headers)


@pytest.fixture
def fake_response():
    """Factory fixture for building fake responses."""
    return make_response


@pytest.fixture
def mock_urlopen():
    """Patch ``urllib.request.urlopen`` and return the mock for configuration."""
    with patch("urllib.request.urlopen") as m:
        yield m