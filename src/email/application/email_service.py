from typing import Text
from ..domain.models.message import TemplateMessage
from ..domain.interfaces.message_sender_interface import MessageSenderInterface


class EmailService:

    def __init__(self, message_sender: MessageSenderInterface) -> None:
        self._message_sender = message_sender

    def send_template_message(self, message: TemplateMessage) -> None:
        self._message_sender.send(message)

    def preview_template_message(self, message: TemplateMessage) -> Text:
        return self._message_sender.render_content(message)[1]