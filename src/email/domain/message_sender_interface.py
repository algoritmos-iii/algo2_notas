from abc import ABC, abstractmethod
from ..domain.message import TemplateMessage

class MessageSenderInterface(ABC):
    @abstractmethod
    def send(self, message: TemplateMessage) -> None:
        ...
