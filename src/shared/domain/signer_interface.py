from abc import ABC, abstractmethod
from typing import Any


class BadData(Exception):
    """
    Exception to be raised in case something has gone wrong
    when decoding data.
    It can mean that the data has been tampered.
    """

    def __init__(self, signed_data: str) -> None:
        self.signed_data = signed_data
        super().__init__()


class SignerInterface(ABC):
    """
    Signs objects in order to verify that data sent from the
    server hasn't been tampered by the user.
    """

    @abstractmethod
    def __init__(self, secret_key: str) -> None:
        ...

    @abstractmethod
    def sign(self, data: Any) -> str:
        """Signs an object using the secret key."""
        ...

    @abstractmethod
    def unsign(self, signed_data: str) -> Any:
        """Decodes the data and verifies the signature."""
        ...
