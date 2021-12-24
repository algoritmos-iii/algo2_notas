from typing import List

from ..domain.models.normal_email import NormalEmail
from ..domain.interfaces.email_sender_interface import EmailSenderInterface


class MockEmailSender(EmailSenderInterface):
    def __init__(
        self,
        gmail_username: str,
        gmail_password: str,
    ) -> None:
        pass

    def send_multiple(self, emails: List[NormalEmail]):
        for email in emails:
            print("=" * 10)
            print(f"To addr: {email.to_addr}")
            print(f"Subject: {email.subject}")
            print(f"BCC: {email.bcc}")
            print("Plaintext content:")
            print(email.plaintext)
            print("=" * 10)
            print()

    def send(self, email: NormalEmail):
        self.send_multiple([email])
