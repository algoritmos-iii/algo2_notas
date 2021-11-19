from src.grades.application.grades_service import GradesService
from src.email.application.email_service import EmailService
from src.email.domain.models.message import TemplateMessage
from src.grades.domain.models.correction import ExamCorrection, IndividualCorrection


class ExamsEmailView:
    def __init__(
        self, grades_service: GradesService, email_service: EmailService
    ) -> None:
        self._grades_service = grades_service
        self._email_service = email_service

    def _message_from_correction(self, individual_correction: ExamCorrection):
        exam_name = individual_correction.correction.activity_name
        return TemplateMessage(
            subject=f"Corrección de {exam_name} - Padrón {individual_correction.individual.padron}",
            to=individual_correction.individual.email,
            template_name="notas_examen",
            context={
                "examen": exam_name,
                "nombre": individual_correction.individual.full_name,
                "corrector": individual_correction.correction.corrector_name,
                "correcciones": individual_correction.correction.details,
                "nota": float(individual_correction.correction.grade.replace(",", ".")),
                "puntos_extras": float(individual_correction.exam_data["extra_points"].replace(",", ".")),
                "nota_final": float(individual_correction.exam_data["final_grade"].replace(",", ".")),
            },
            with_copy_to_docentes=True,
        )

    def send(self, exam_name: str):
        for individual_correction in self._grades_service.get_exam_feedback_by_name(
            exam_name
        ):
            self._email_service.send_template_message(
                self._message_from_correction(individual_correction)
            )

        return exam_name

    def preview(self, exam_name: str, padron_number: str):
        for individual_correction in self._grades_service.get_exam_feedback_by_name(
            exam_name
        ):
            print(individual_correction)
            if individual_correction.individual.padron == padron_number:
                return self._email_service.preview_template_message(
                    self._message_from_correction(individual_correction)
                )
        return "Non a valid padron"
