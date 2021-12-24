from typing import Any, Dict

from ..domain.interfaces.templater_interface import TemplaterInterface
from ..domain.models.template_email_builder_base import TemplateEmailBuilderBase


class LoginEmailBuilder(TemplateEmailBuilderBase):
    TEMPLATE_PLAIN_DIR = "emails/sign_in_plain.html"
    TEMPLATE_HTML_DIR = "emails/sign_in.html"
    WITH_COPY_TO_DOCENTES = False

    def _create_subject(self) -> str:
        return "Enlace para consultar las notas"

    def _create_context(self, login_url: str) -> Dict[str, Any]:
        return {"enlace": login_url}

    def create_email(self, to_addr: str, login_url: str):
        return super().create_email(
            to_addr=to_addr,
            subject=self._create_subject(),
            context=self._create_context(login_url),
        )
