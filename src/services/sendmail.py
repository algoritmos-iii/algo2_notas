#!/usr/bin/env python3
from __future__ import annotations

import base64
import smtplib
from email.message import EmailMessage
from email.utils import formatdate
from typing import TYPE_CHECKING, Iterable, List, Optional

if TYPE_CHECKING:
    from ..api.google_credentials import GoogleCredentials

SendmailException = smtplib.SMTPException


class Email:
    def __init__(self, subject: str,
                 from_addr: str,
                 to_addr: str,
                 cc: Optional[str] = None,
                 bcc: Optional[str] = None,
                 reply_to: Optional[str] = None) -> None:
        msg = EmailMessage()
        msg.set_charset("uft-8")
        msg["Date"] = formatdate(localtime=True)
        msg["Subject"] = subject
        msg["From"] = from_addr
        msg["To"] = to_addr
        if cc:
            msg["CC"] = cc
        if bcc:
            msg["BCC"] = bcc
        if reply_to:
            msg["Reply-to"] = reply_to

        self._msg = msg

    @property
    def message(self) -> EmailMessage:
        return self._msg

    def add_plaintext_content(self, content: str) -> None:
        self._msg.set_content(content)

    def add_html_content(self, content: str) -> None:
        if self._msg.get_content() is None:
            raise Exception(
                "Email has no plaintext content. It should be added before adding an html part")

        self._msg.add_alternative(content, subtype='html')


class EmailSender:
    def __init__(self, gmail_user: str, google_credentials: GoogleCredentials) -> None:
        self._account = gmail_user
        self._google_credentials = google_credentials

    def _encoded_credentials(self) -> bytes:
        creds = self._google_credentials.get_credenciales_email()
        xoauth2_tok = f"user={self._account}\1auth=Bearer {creds.access_token}\1\1".encode(
            "utf-8")

        return xoauth2_tok

    def send_mail(self, email: Email) -> None:
        self.send_batch_mail([email])

    def send_batch_mail(self, emails: Iterable[Email]) -> None:
        try:
            iter(emails)
        except TypeError:
            emails: Iterable[Email] = [
                emails] if emails is not List else emails

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.docmd("AUTH", "XOAUTH2 " +
                         base64.b64encode(self._encoded_credentials()).decode("utf-8"))

            for email in emails:
                server.send_message(email.message)

class AppPasswordEmailSender:
    def __init__(self, gmail_username: str, gmail_password: str) -> None:
        self._gmail_username = gmail_username
        self._gmail_password = gmail_password

    def send_mail(self, email: Email) -> None:
        self.send_batch_mail([email])

    def send_batch_mail(self, emails: Iterable[Email]) -> None:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(self._gmail_username, self._gmail_password)
            for email in emails:
                server.send_message(email.message)