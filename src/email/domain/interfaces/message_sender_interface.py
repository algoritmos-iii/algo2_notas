from abc import ABC, abstractmethod
from typing import Text
from ..models.message import TemplateMessage

class MessageSenderInterface(ABC):
    @abstractmethod
    def send(self, message: TemplateMessage) -> None:
        ...

    @abstractmethod
    def render_content(self, message: TemplateMessage) -> tuple[Text, Text]:
        ...
