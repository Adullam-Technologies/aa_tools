"""Friendly error types for aa_agent_tools."""

from __future__ import annotations


class AAError(Exception):
    """Base class for every error aa_agent_tools can raise."""


class AARequestError(AAError):
    """Raised when a web request comes back with an HTTP error status."""

    def __init__(self, status: int, reason: str, body: str = ""):
        self.status = status
        self.reason = reason
        self.body = body
        hint = ""
        if status == 401:
            hint = " (did you forget your API key, or is it wrong?)"
        elif status == 403:
            hint = " (this key is not allowed to do that)"
        elif status == 404:
            hint = " (nothing was found at that address)"
        elif status == 429:
            hint = " (you've hit a rate limit - wait a moment and try again)"
        super().__init__(f"HTTP {status} {reason}{hint}".strip())


class AAMissingKeyError(AAError):
    """Raised when a required API key was not supplied."""

    def __init__(self, name: str):
        self.key_name = name
        super().__init__(
            f"Missing API key: {name}. Pass it as an argument, e.g. {name}='YOUR_KEY'."
        )
