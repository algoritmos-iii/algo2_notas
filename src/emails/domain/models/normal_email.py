from typing import List, Optional, Union
from dataclasses import dataclass


@dataclass
class NormalEmail:
    from_addr: str
    to_addr: Union[List[str], str]
    subject: str
    plaintext: str
    html: str
    reply_to: Optional[str]
    bcc: Optional[str] = None
