from abc import ABC, abstractmethod
from ..models.message import TemplateMessage

class MessageSenderInterface(ABC):
    @abstractmethod
    def send(self, message: TemplateMessage) -> None:
        ...
