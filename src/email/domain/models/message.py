from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

@dataclass
class TemplateMessage:
    template_name: str
    to: Union[str, List[str]]
    subject: str
    context: Dict[str, Any]
    with_copy_to_docentes: bool = False

@dataclass
class Message:
    subject: str
    to: Union[str, List[str]]
    cc: Union[str, List[str], None]
    reply_to: Optional[str]
    plaintext_content: str
    html_content: str