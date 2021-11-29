from abc import ABC, abstractmethod
from ..models.message import EmailIntent


class MessageSenderInterface(ABC):
    @abstractmethod
    def send(self, message: EmailIntent) -> None:
        ...
