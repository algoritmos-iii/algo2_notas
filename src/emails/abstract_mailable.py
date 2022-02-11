from email.message import EmailMessage
from typing import Dict, Optional


class MissingHeadersException(ValueError):
    def __init__(self, missing_headers) -> None:
        super().__init__(f"Missing the following headers: {', '.join(missing_headers)}")

        self.missing_headers = missing_headers


class AbstractMailable:
    _REQUIRED_HEADERS = ["from", "to", "subject"]

    def __init__(self) -> None:
        self._headers: Dict[str, Optional[str]] = {}

    # MAIN HEADERS

    def set_from(self, from_addr: str):
        self._headers["from"] = from_addr
        return self

    def set_subject(self, subject: str):
        self._headers["subject"] = subject
        return self

    def set_recipients(self, recipients: str):
        self._headers["to"] = recipients
        return self

    def set_cc(self, cc_addresses: Optional[str]):
        self._headers["cc"] = cc_addresses
        return self

    # CONTENT

    def set_plaintext_content(self, plaintext_content: str):
        self._headers["plaintext"] = plaintext_content
        return self

    def set_html_content(self, html_content: str):
        self._headers["html"] = html_content
        return self

    # EMAIL BUILDING

    def _is_field_set(self, field_name: str) -> bool:
        return (field_name in self._headers) and bool(self._headers[field_name])

    def generate_email_message(self) -> EmailMessage:
        missing_required_headers = [
            required_header
            for required_header in self._REQUIRED_HEADERS
            if required_header not in self._headers.keys()
        ]

        if missing_required_headers:
            raise MissingHeadersException(missing_required_headers)

        msg = EmailMessage()
        msg["From"] = self._headers["from"]
        msg["To"] = self._headers["to"]
        msg["Subject"] = self._headers["subject"]

        if self._is_field_set("cc"):
            msg["CC"] = self._headers["cc"]

        if self._is_field_set("plaintext"):
            msg.set_content(self._headers["plaintext"])

        if self._is_field_set("html"):
            msg.add_alternative(self._headers["html"], subtype="html")

        return msg
