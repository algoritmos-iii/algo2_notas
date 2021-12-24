import smtplib
from typing import List

from .smtp_email import SmtpEmail

from ..domain.models.normal_email import NormalEmail
from ..domain.interfaces.email_sender_interface import EmailSenderInterface


class EmailSender(EmailSenderInterface):
    def __init__(
        self,
        gmail_username: str,
        gmail_password: str,
    ) -> None:
        self._gmail_username = gmail_username
        self._gmail_password = gmail_password

    def send_multiple(self, emails: List[NormalEmail]):
        smtp_emails = (SmtpEmail.from_email(email) for email in emails)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(self._gmail_username, self._gmail_password)
            for email in smtp_emails:
                server.send_message(email.message())

    def send(self, email: NormalEmail):
        self.send_multiple([email])
