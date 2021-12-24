from typing import Any, Dict, List, Optional, Union
from abc import ABC, abstractmethod

from .normal_email import NormalEmail
from ..interfaces.templater_interface import TemplaterInterface


class TemplateEmailBuilderBase(ABC):
    TEMPLATE_PLAIN_DIR: Optional[str] = None
    TEMPLATE_HTML_DIR: Optional[str] = None
    WITH_COPY_TO_DOCENTES: Optional[bool] = None

    def __init__(
        self,
        templater: TemplaterInterface,
        from_addr: str,
        docentes_email: str,
    ) -> None:
        self._assert_class_variables()

        self._templater = templater
        self._from_addr = from_addr
        self._docentes_email = docentes_email

    # PRIVATE MESSAGES
    def _assert_class_variables(self):
        assert self.TEMPLATE_PLAIN_DIR is not None
        assert self.TEMPLATE_HTML_DIR is not None
        assert self.WITH_COPY_TO_DOCENTES is not None

    # PUBLIC PROTOCOL
    def _render_plaintext(self, context: Dict[str, Any]) -> str:
        return self._templater.render(self.TEMPLATE_PLAIN_DIR, context)

    def _render_html(self, context: Dict[str, Any]) -> str:
        return self._templater.render(self.TEMPLATE_HTML_DIR, context)

    @abstractmethod
    def create_email(
        self,
        to_addr: Union[List[str], str],
        subject: str,
        context: Dict[str, Any],
    ) -> NormalEmail:
        return NormalEmail(
            from_addr=self._from_addr,
            to_addr=to_addr,
            subject=subject,
            reply_to=self._docentes_email,
            bcc=self._docentes_email if self.WITH_COPY_TO_DOCENTES else None,
            plaintext=self._render_plaintext(context),
            html=self._render_html(context),
        )
