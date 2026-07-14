"""Tests for aa_tools.email_tools."""

from __future__ import annotations

from email.message import EmailMessage
from unittest.mock import MagicMock, patch

import pytest

from aa_tools import email_tools
from aa_tools.errors import AAMissingKeyError


class TestSendEmail:
    def test_requires_username(self):
        with pytest.raises(AAMissingKeyError):
            email_tools.send_email("a@b.com", "subj", "body", smtp_host="smtp.x.com", username="", password="x")

    def test_requires_password(self):
        with pytest.raises(AAMissingKeyError):
            email_tools.send_email("a@b.com", "subj", "body", smtp_host="smtp.x.com", username="u", password="")

    @patch("aa_tools.email_tools.smtplib.SMTP")
    def test_success_with_tls(self, mock_smtp):
        server = MagicMock()
        mock_smtp.return_value.__enter__ = MagicMock(return_value=server)
        mock_smtp.return_value.__exit__ = MagicMock(return_value=False)

        result = email_tools.send_email(
            "friend@example.com", "Hello", "Body text",
            smtp_host="smtp.example.com", smtp_port=587,
            username="me@example.com", password="pass",
        )
        assert result == "Email sent to friend@example.com"
        mock_smtp.assert_called_once_with("smtp.example.com", 587, timeout=30)
        server.starttls.assert_called_once()
        server.login.assert_called_once_with("me@example.com", "pass")
        server.send_message.assert_called_once()

    @patch("aa_tools.email_tools.smtplib.SMTP")
    def test_no_tls(self, mock_smtp):
        server = MagicMock()
        mock_smtp.return_value.__enter__ = MagicMock(return_value=server)
        mock_smtp.return_value.__exit__ = MagicMock(return_value=False)

        email_tools.send_email(
            "to@x.com", "S", "B",
            smtp_host="h", smtp_port=25,
            username="u", password="p", use_tls=False,
        )
        server.starttls.assert_not_called()

    @patch("aa_tools.email_tools.smtplib.SMTP")
    def test_from_addr_defaults_to_username(self, mock_smtp):
        server = MagicMock()
        mock_smtp.return_value.__enter__ = MagicMock(return_value=server)
        mock_smtp.return_value.__exit__ = MagicMock(return_value=False)

        email_tools.send_email(
            "to@x.com", "S", "B",
            smtp_host="h", username="me@x.com", password="p",
        )
        sent_msg = server.send_message.call_args[0][0]
        assert sent_msg["From"] == "me@x.com"

    @patch("aa_tools.email_tools.smtplib.SMTP")
    def test_custom_from_addr(self, mock_smtp):
        server = MagicMock()
        mock_smtp.return_value.__enter__ = MagicMock(return_value=server)
        mock_smtp.return_value.__exit__ = MagicMock(return_value=False)

        email_tools.send_email(
            "to@x.com", "S", "B",
            smtp_host="h", username="me@x.com", password="p",
            from_addr="custom@x.com",
        )
        sent_msg = server.send_message.call_args[0][0]
        assert sent_msg["From"] == "custom@x.com"

    @patch("aa_tools.email_tools.smtplib.SMTP")
    def test_email_content_set_correctly(self, mock_smtp):
        server = MagicMock()
        mock_smtp.return_value.__enter__ = MagicMock(return_value=server)
        mock_smtp.return_value.__exit__ = MagicMock(return_value=False)

        email_tools.send_email(
            "to@x.com", "My Subject", "My Body",
            smtp_host="h", username="u@x.com", password="p",
        )
        sent_msg = server.send_message.call_args[0][0]
        assert sent_msg["Subject"] == "My Subject"
        assert sent_msg["To"] == "to@x.com"


class TestSendEmailGmail:
    @patch("aa_tools.email_tools.smtplib.SMTP")
    def test_delegates_to_send_email(self, mock_smtp):
        server = MagicMock()
        mock_smtp.return_value.__enter__ = MagicMock(return_value=server)
        mock_smtp.return_value.__exit__ = MagicMock(return_value=False)

        result = email_tools.send_email_gmail(
            "friend@example.com", "Hi", "Body",
            gmail="me@gmail.com", app_password="abcd efgh ijkl mnop",
        )
        assert result == "Email sent to friend@example.com"
        mock_smtp.assert_called_once_with("smtp.gmail.com", 587, timeout=30)
        server.login.assert_called_once_with("me@gmail.com", "abcd efgh ijkl mnop")

    @patch("aa_tools.email_tools.smtplib.SMTP")
    def test_from_addr_set_to_gmail(self, mock_smtp):
        server = MagicMock()
        mock_smtp.return_value.__enter__ = MagicMock(return_value=server)
        mock_smtp.return_value.__exit__ = MagicMock(return_value=False)

        email_tools.send_email_gmail("to@x.com", "S", "B", gmail="me@gmail.com", app_password="p")
        sent_msg = server.send_message.call_args[0][0]
        assert sent_msg["From"] == "me@gmail.com"