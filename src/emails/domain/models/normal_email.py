from typing import List, Optional, Union
from dataclasses import dataclass


@dataclass
class NormalEmail:
    from_addr: str
    to_addr: Union[List[str], str]
    subject: str
    reply_to: str
    plaintext: str
    html: str
    bcc: Optional[str] = None
