from abc import ABC, abstractmethod
from typing import List

from ..models.normal_email import NormalEmail


class EmailSenderInterface(ABC):
    @abstractmethod
    def send_multiple(self, email: List[NormalEmail]) -> None:
        ...

    @abstractmethod
    def send(self, email: NormalEmail) -> None:
        ...
