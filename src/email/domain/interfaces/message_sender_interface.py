from abc import ABC, abstractmethod
from ..models.message import Message

class MessageSenderInterface(ABC):
    @abstractmethod
    def send(self, message: Message) -> None:
        ...