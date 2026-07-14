"""Live tests for aa_tools.email_tools (Gmail SMTP).

These send a **real email** and need Gmail credentials. Run with::

    uv run pytest --live -m live tests/test_email_live.py
"""

from __future__ import annotations

import pytest

from aa_tools import email_tools


pytestmark = pytest.mark.live


class TestSendEmailGmailLive:
    def test_send_real_email(self, gmail_address, gmail_app_password, email_to):
        if not (gmail_address and gmail_app_password and email_to):
            pytest.skip("GMAIL_ADDRESS / GMAIL_APP_PASSWORD / TO not set")
        result = email_tools.send_email_gmail(
            to=email_to,
            subject="aa_tools live test ✅",
            body=(
                "This is an automated test email from the aa_tools test-suite.\n\n"
                "If you received this, the send_email_gmail() function works!"
            ),
            gmail=gmail_address,
            app_password=gmail_app_password,
        )
        assert result == f"Email sent to {email_to}"