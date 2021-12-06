from ..domain.models.email_intent import EmailIntent
from .email_message_sender import EmailMessageSender


class MockEmailMessageSender(EmailMessageSender):
    def send(self, message: EmailIntent):
        print(message)
