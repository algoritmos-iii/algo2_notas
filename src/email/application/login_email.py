from dataclasses import dataclass
from typing import Any, Dict
from .email_base import EmailBase


@dataclass
class LoginData:
    login_url: str


@dataclass
class LoginEmailData:
    student_email: str
    login_data: LoginData


class LoginEmail(EmailBase):
    TEMPLATE_PLAIN_DIR = "emails/sign_in_plain.html"
    TEMPLATE_HTML_DIR = "emails/sign_in.html"
    WITH_COPY_TO_DOCENTES = False

    def _create_subject(self) -> str:
        return "Enlace para consultar las notas"

    def _create_context(self, data: LoginData) -> Dict[str, Any]:
        return {"enlace": data.login_url}

    def send_email(self, data: LoginEmailData) -> None:
        subject = self._create_subject()
        context = self._create_context(data.login_data)

        message = self._create_message(data.student_email, subject, context)
        self._message_sender.send(message)
