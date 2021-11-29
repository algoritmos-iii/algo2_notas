from dataclasses import dataclass
from typing import List, Optional, Union


@dataclass
class EmailIntent:
    subject: str
    to: Union[str, List[str]]
    cc: Union[str, List[str], None]
    reply_to: Optional[str]
    plaintext_content: str
    html_content: str
