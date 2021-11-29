from abc import ABC, abstractmethod
from ..models.email_intent import EmailIntent


class MessageSenderInterface(ABC):
    @abstractmethod
    def send(self, message: EmailIntent) -> None:
        ...
