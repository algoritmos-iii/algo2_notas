from typing import Text

from ..domain.interfaces.message_sender_interface import MessageSenderInterface
from ..domain.interfaces.templater_interface import TemplaterInterface
from ..domain.models.message import Message, TemplateMessage


class EmailService:

    docentes_email = (
        '"Docentes Algoritmos 3" <fiuba-algoritmos-iii-doc@googlegroups.com>'
    )

    def __init__(
        self, message_sender: MessageSenderInterface, templater: TemplaterInterface
    ) -> None:
        self._message_sender = message_sender
        self._templater = templater

    def _render_plain_template(self, message: TemplateMessage):
        return self._templater.render(
            template_name=f"emails/{message.template_name}_plain.html",
            context=message.context,
        )

    def _render_html_template(self, message: TemplateMessage):
        return self._templater.render(
            template_name=f"emails/{message.template_name}.html",
            context=message.context,
        )

    def _template_message_to_message(self, message: TemplateMessage):
        return Message(
            subject=message.subject,
            to=message.to,
            cc=self.docentes_email if message.with_copy_to_docentes else None,
            reply_to=self.docentes_email,
            plaintext_content=self._render_plain_template(message),
            html_content=self._render_html_template(message),
        )

    def send_template_message(self, template_message: TemplateMessage) -> None:
        message = self._template_message_to_message(template_message)
        self._message_sender.send(message)

    def preview_template_message(self, message: TemplateMessage) -> Text:
        return self._render_html_template(message)
