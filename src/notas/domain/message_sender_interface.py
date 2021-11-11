from abc import ABC, abstractmethod
from ..domain.student import StudentInfo
from ..domain.messages.base_message import BaseMessage


class MessageSenderInterface(ABC):
    @abstractmethod
    def send(self, student: StudentInfo, message: BaseMessage) -> None:
        ...
