from typing import List, Optional, Union
from email.message import EmailMessage
from email.utils import formatdate

from ..domain.models.normal_email import NormalEmail


SingleOrMultipleRecipient = Union[List[str], str]


def _parse_header(header: Optional[SingleOrMultipleRecipient]) -> Optional[str]:
    if header is None:
        return None
    elif isinstance(header, str):
        return header

    return ",".join(header)


class SmtpEmail:
    """
    An OOP abstraction of an SMTP email
    """

    def __init__(
        self,
        subject: str,
        from_addr: str,
        to_addr: SingleOrMultipleRecipient,
        cc: Optional[SingleOrMultipleRecipient] = None,
        bcc: Optional[SingleOrMultipleRecipient] = None,
        reply_to: Optional[SingleOrMultipleRecipient] = None,
    ) -> None:
        # Parse headers
        to_addr: str = _parse_header(to_addr)
        cc = _parse_header(cc)
        bcc = _parse_header(bcc)
        reply_to = _parse_header(reply_to)

        # Create message
        msg = EmailMessage()
        msg.set_charset("uft-8")
        msg["Date"] = formatdate(localtime=True)
        msg["Subject"] = subject
        msg["From"] = from_addr
        msg["To"] = _parse_header(to_addr)
        if cc:
            msg["CC"] = cc
        if bcc:
            msg["BCC"] = bcc
        if reply_to:
            msg["Reply-to"] = reply_to

        self._msg = msg

    @classmethod
    def from_email(cls, email: NormalEmail):
        smtp_email = SmtpEmail(
            from_addr=email.from_addr,
            to_addr=email.to_addr,
            subject=email.subject,
            reply_to=email.reply_to,
            bcc=email.bcc,
        )
        smtp_email.add_plaintext_content(email.plaintext)
        smtp_email.add_html_content(email.html)
        return smtp_email

    def message(self) -> EmailMessage:
        return self._msg

    def add_plaintext_content(self, content: str) -> None:
        self._msg.set_content(content)

    def add_html_content(self, content: str) -> None:
        if self._msg.get_content() is None:
            raise Exception(
                "Email has no plaintext content. It should be added before adding an html part"
            )

        self._msg.add_alternative(content, subtype="html")