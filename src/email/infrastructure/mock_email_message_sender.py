from ..domain.models.message import TemplateMessage
from .email_message_sender import EmailMessageSender


class MockEmailMessageSender(EmailMessageSender):
    def send(self, message: TemplateMessage):
        print(message)
