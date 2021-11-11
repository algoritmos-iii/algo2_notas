from dataclasses import dataclass
from .base_message import BaseMessage

@dataclass
class LoginMessage(BaseMessage):
    login_link: str
