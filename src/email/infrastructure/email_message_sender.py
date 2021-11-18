import smtplib
from typing import Text, Tuple
import jinja2

from .email import Email
from ..domain.models.message import TemplateMessage
from ..domain.interfaces.message_sender_interface import MessageSenderInterface


class EmailMessageSender(MessageSenderInterface):
    docentes_email = "Docentes Algoritmos 3 <fiuba-algoritmos-iii-doc@googlegroups.com>"

    def __init__(
        self,
        gmail_username: str,
        gmail_password: str,
        templater: jinja2.Environment,
    ) -> None:
        self._gmail_username = gmail_username
        self._gmail_password = gmail_password
        self._templater = templater
        self.from_addr = f"Algoritmos3Leveroni <{gmail_username}>"

    def render_content(self, message: TemplateMessage) -> Tuple[Text, Text]:
        plain_template = self._templater.get_template(
            f"emails/{message.template_name}_plain.html"
        )
        html_template = self._templater.get_template(
            f"emails/{message.template_name}.html"
        )

        return (
            plain_template.render(**message.context),
            html_template.render(**message.context),
        )

    def _create_email(self, message: TemplateMessage):
        to_addr = message.to if isinstance(message.to, str) else ",".join(message.to)
        plain_content, html_content = self.render_content(message)
        email = Email(
            from_addr=self.from_addr,
            subject=message.subject,
            to_addr=to_addr,
            reply_to=self.docentes_email,
            cc=self.docentes_email if message.with_copy_to_docentes else None,
        )
        email.add_plaintext_content(plain_content)
        email.add_html_content(html_content)
        return email

    def send(self, message: TemplateMessage):
        email = self._create_email(message).message

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(self._gmail_username, self._gmail_password)
            server.send_message(
                msg=email,
                from_addr=self.from_addr,
                to_addrs=message.to,
            )
