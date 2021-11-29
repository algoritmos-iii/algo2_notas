import smtplib
from typing import List, Union

from .email import Email

from ..domain.models.email_intent import EmailIntent
from ..domain.interfaces.message_sender_interface import MessageSenderInterface


class EmailMessageSender(MessageSenderInterface):
    def __init__(
        self,
        gmail_username: str,
        gmail_password: str,
    ) -> None:
        self._gmail_username = gmail_username
        self._gmail_password = gmail_password
        self.from_addr = f"Algoritmos3Leveroni <{gmail_username}>"

    def _email_address_to_header(self, addr: Union[str, List[str], None]):
        if not addr:
            return None
        elif isinstance(addr, str):
            return addr
        else:
            return ",".join(addr)

    def _create_email(self, message: EmailIntent):
        email = Email(
            from_addr=self.from_addr,
            subject=message.subject,
            to_addr=self._email_address_to_header(message.to),
            cc=self._email_address_to_header(message.cc),
            reply_to=self._email_address_to_header(message.reply_to),
        )
        email.add_plaintext_content(message.plaintext_content)
        email.add_html_content(message.html_content)
        return email

    def send(self, message: EmailIntent):
        email = self._create_email(message).message

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(self._gmail_username, self._gmail_password)
            server.send_message(email)
