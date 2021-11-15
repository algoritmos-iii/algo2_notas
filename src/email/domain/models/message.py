from dataclasses import dataclass
from typing import Any, Dict, List, Union

@dataclass
class TemplateMessage:
    template_name: str
    to: Union[str, List[str]]
    subject: str
    context: Dict[str, Any]
    with_copy_to_docentes: bool = False