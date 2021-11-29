from dataclasses import dataclass
from typing import Any, Dict, List
from .email_base import EmailBase


@dataclass
class ExerciseData:
    exercise_name: str
    group_number: str
    corrector_name: str
    grade: str
    correction_details: str


@dataclass
class ExerciseEmailData:
    student_emails: List[str]
    exercise_data: ExerciseData


class ExerciseEmail(EmailBase):
    TEMPLATE_PLAIN_DIR = "emails/notas_ejercicio_plain.html"
    TEMPLATE_HTML_DIR = "emails/notas_ejercicio.html"
    WITH_COPY_TO_DOCENTES = True

    def _create_subject(self, data: ExerciseData) -> str:
        return (
            f"Corrección de ejercicio {data.exercise_name} - Grupo {data.group_number}"
        )

    def _create_context(self, data: ExerciseData) -> Dict[str, Any]:
        return {
            "ejercicio": data.exercise_name,
            "grupo": data.group_number,
            "corrector": data.corrector_name,
            "nota": float(data.grade.replace(",", ".")),
            "correcciones": data.correction_details,
        }

    def send_email(self, data: ExerciseEmailData) -> None:
        subject = self._create_subject(data.exercise_data)
        context = self._create_context(data.exercise_data)

        message = self._create_message(data.student_emails, subject, context)
        self._message_sender.send(message)

    def preview_email(self, data: ExerciseEmailData) -> str:
        context = self._create_context(data.exercise_data)
        return self._render_html(context)
