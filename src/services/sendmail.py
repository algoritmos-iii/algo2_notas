#!/usr/bin/env python3
from __future__ import annotations

import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from jinja2 import Environment
from contextlib import contextmanager
from typing import Optional, Sequence, Union

from ..api.google_credentials import GoogleCredentials

SendmailException = smtplib.SMTPException


class EmailSender:
    def __init__(self, jinja2_env: Environment, google_credentials: GoogleCredentials, from_name: str, from_email: str) -> None:
        self._account = from_email
        self._google_credentials = google_credentials
        self._encoded_from_email = "{} <{}>".format(from_name, from_email)
        self._jinja2_env = jinja2_env

    def _encoded_credentials(self) -> bytes:
        creds = self._google_credentials.get_credenciales_email()
        xoauth2_tok = f"user={self._account}\1auth=Bearer {creds.access_token}\1\1".encode(
            "utf-8")

        return xoauth2_tok

    @contextmanager
    def _connection(self):
        # Connect to SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.docmd("AUTH", "XOAUTH2 " +
                     base64.b64encode(self._encoded_credentials()).decode("utf-8"))

        try:
            yield server
        finally:
            server.close()

    def _create_mail(self, template_path: str, subject: str, to_addr: Sequence[str], **kwargs) -> MIMEText:
        template = self._jinja2_env.get_template(template_path)

        msg = MIMEText(template.render(**kwargs), _charset="utf-8")
        msg["Subject"] = subject
        msg["From"] = self._encoded_from_email
        msg["To"] = ", ".join(to_addr)
        msg["Date"] = formatdate(localtime=True)

        return msg

    def _create_rich_mail(self, subject: str, to_addr: Sequence[str], plaintext_message: str, html_message: str) -> MIMEMultipart:

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self._encoded_from_email
        message["To"] = ", ".join(to_addr)
        message["Date"] = formatdate(localtime=True)

        plaintext = MIMEText(plaintext_message, "plain")
        html = MIMEText(html_message, "html")

        message.attach(plaintext)
        message.attach(html)

        return message

    def send_mail(self, template_path: str, subject: str, to_addr: Union[str, Sequence[str]], **kwargs) -> None:

        if isinstance(to_addr, str):
            to_addr = [to_addr]

        with self._connection() as server:
            msg = self._create_mail(template_path, subject, to_addr, **kwargs)
            server.sendmail(self._account, to_addr, msg.as_string())

    def send_html_mail(self, subject: str, to_addr: Sequence[str], plaintext_message: str, html_message: str) -> None:

        if isinstance(to_addr, str):
            to_addr = [to_addr]

        with self._connection() as server:
            message = self._create_rich_mail(subject, to_addr,
                                         plaintext_message, html_message)
            server.sendmail(self._account, to_addr, message.as_string())
