from abc import ABC, abstractmethod
from typing import List

from ..models.normal_email import NormalEmail


class EmailSenderInterface(ABC):
    """
    Establishes an interface for an email sender.
    An email sender is an object in charge of sending emails (`NormalEmail`).
    """

    @abstractmethod
    def send_multiple(self, email: List[NormalEmail]) -> None:
        """
        Sends multiple emails. When they are many, it is more efficient than
        using multiple calls to `send`.
        """
        ...

    @abstractmethod
    def send(self, email: NormalEmail) -> None:
        """Sends a single email."""
        ...
