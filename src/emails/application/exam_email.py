from typing import Any, Dict
from dataclasses import dataclass

from ..domain.models.template_email_builder_base import TemplateEmailBuilderBase


@dataclass
class ExamData:
    exam_name: str
    student_padron: str
    student_full_name: str
    corrector_name: str
    correction_details: str
    grade: float
    extra_points: float
    final_grade: float


class ExamEmailBuilder(TemplateEmailBuilderBase):
    TEMPLATE_PLAIN_DIR = "emails/notas_examen_plain.html"
    TEMPLATE_HTML_DIR = "emails/notas_examen.html"
    WITH_COPY_TO_DOCENTES = True

    def _create_subject(self, data: ExamData) -> str:
        return f"Corrección de {data.exam_name} - Padrón {data.student_padron}"

    def _create_context(self, data: ExamData) -> Dict[str, Any]:
        return {
            "examen": data.exam_name,
            "nombre": data.student_full_name,
            "corrector": data.corrector_name,
            "correcciones": data.correction_details,
            "nota": data.grade,
            "puntos_extras": data.extra_points,
            "nota_final": data.final_grade,
        }

    def html_part(self, data: ExamData) -> str:
        context = self._create_context(data)
        return super()._render_html(context)

    def create_email(self, to_addr: str, data: ExamData):
        return super().create_email(
            to_addr=to_addr,
            subject=self._create_subject(data),
            context=self._create_context(data),
        )
