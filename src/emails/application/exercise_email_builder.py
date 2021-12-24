from dataclasses import dataclass
from typing import Any, Dict, List

from ..domain.models.template_email_builder_base import TemplateEmailBuilderBase


@dataclass
class ExerciseData:
    exercise_name: str
    group_number: str
    corrector_name: str
    grade: str
    correction_details: str


class ExerciseEmailBuilder(TemplateEmailBuilderBase):
    TEMPLATE_PLAIN_DIR = "emails/notas_ejercicio_plain.html"
    TEMPLATE_HTML_DIR = "emails/notas_ejercicio.html"
    WITH_COPY_TO_DOCENTES = True

    def _create_subject(self, data: ExerciseData):
        return (
            f"Corrección de ejercicio {data.exercise_name} - Grupo {data.group_number}"
        )

    def _create_context(self, data: ExerciseData) -> Dict[str, Any]:
        return {
            "ejercicio": data.exercise_name,
            "grupo": data.group_number,
            "corrector": data.corrector_name,
            "nota": data.grade,
            "correcciones": data.correction_details,
        }

    def html_part(self, exercise_email_data: ExerciseData) -> str:
        context = self._create_context(exercise_email_data)
        return super()._render_html(context)

    def create_email(self, to_addr: List[str], exercise_email_data: ExerciseData):
        return super().create_email(
            to_addr=to_addr,
            subject=self._create_subject(exercise_email_data),
            context=self._create_context(exercise_email_data),
        )
