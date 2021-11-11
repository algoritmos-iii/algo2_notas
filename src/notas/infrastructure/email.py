from typing import Optional
from email.message import EmailMessage
from email.utils import formatdate


class Email:
    def __init__(
        self,
        subject: str,
        # from_addr: str,
        # to_addr: str,
        cc: Optional[str] = None,
        bcc: Optional[str] = None,
        reply_to: Optional[str] = None,
    ) -> None:
        msg = EmailMessage()
        msg.set_charset("uft-8")
        msg["Date"] = formatdate(localtime=True)
        msg["Subject"] = subject
        # msg["From"] = from_addr
        # msg["To"] = to_addr
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
                "Email has no plaintext content. It should be added before adding an html part"
            )

        self._msg.add_alternative(content, subtype="html")
