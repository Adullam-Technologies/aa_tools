"""Send emails from your agent.

Uses only the standard library's ``smtplib`` so it works in Pyodide. You will
need an email account that allows "app passwords" (Gmail, Outlook, etc.).
"""

from __future__ import annotations

import smtplib
import ssl
from email.message import EmailMessage

from ._util import require_key


def send_email(
    to: str,
    subject: str,
    body: str,
    *,
    smtp_host: str,
    smtp_port: int = 587,
    username: str,
    password: str,
    from_addr: str | None = None,
    use_tls: bool = True,
):
    """Send a plain-text email through any SMTP server.

    Parameters
    ----------
    to : str
        Recipient email address.
    subject, body : str
        Email subject and message text.
    smtp_host, smtp_port : str, int
        Your email provider's SMTP server (e.g. ``"smtp.gmail.com"``, port 587).
    username, password : str
        Login + app password (NOT your normal account password).
    from_addr : str | None
        Sender address (defaults to ``username``).

    Example
    -------
    >>> aa.send_email(
    ...     to="friend@example.com",
    ...     subject="Hello from my agent!",
    ...     body="My robot wrote this email.",
    ...     smtp_host="smtp.gmail.com",
    ...     username="you@gmail.com",
    ...     password="app-password-here",
    ... )
    """
    require_key(username, "username")
    require_key(password, "password")
    sender = from_addr or username

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to
    msg.set_content(body)

    with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
        if use_tls:
            context = ssl.create_default_context()
            server.starttls(context=context)
        server.login(username, password)
        server.send_message(msg)
    return f"Email sent to {to}"


def send_email_gmail(to: str, subject: str, body: str, *, gmail: str, app_password: str):
    """Send an email using a Gmail account.

    ``gmail`` is your full address (e.g. ``"you@gmail.com"``) and
    ``app_password`` is a 16-character Gmail app password, not your normal
    password. Make one at https://myaccount.google.com/apppasswords.

    Example
    -------
    >>> aa.send_email_gmail(
    ...     to="friend@example.com",
    ...     subject="hi!",
    ...     body="sent from aa_tools",
    ...     gmail="you@gmail.com",
    ...     app_password="abcd efgh ijkl mnop",
    ... )
    """
    return send_email(
        to,
        subject,
        body,
        smtp_host="smtp.gmail.com",
        smtp_port=587,
        username=gmail,
        password=app_password,
        from_addr=gmail,
        use_tls=True,
    )
