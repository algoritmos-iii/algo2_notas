import flask
from src.grades.application.grades_service import GradesService
from src.email.application.email_service import EmailService
from src.email.domain.models.message import TemplateMessage
from src.grades.domain.models.correction import GroupCorrection


class ExercisesEmailView:
    def __init__(
        self, grades_service: GradesService, email_service: EmailService
    ) -> None:
        self._grades_service = grades_service
        self._email_service = email_service

    def _message_from_correction(self, group_correction: GroupCorrection):
        exercise_name = group_correction.correction.activity_name
        return TemplateMessage(
            subject=f"Corrección de ejercicio {exercise_name}",
            to=group_correction.group.emails,
            template_name="notas_ejercicio",
            context={
                "ejercicio": exercise_name,
                "grupo": group_correction.group.group_number,
                "corrector": group_correction.correction.corrector_name,
                "nota": group_correction.correction.grade,
                "correcciones": group_correction.correction.details,
            },
            with_copy_to_docentes=True,
        )

    def send(self, exercise_name: str):
        for group_correction in self._grades_service.get_exercise_feedback_by_name(
            exercise_name
        ):
            self._email_service.send_template_message(
                self._message_from_correction(group_correction)
            )
        return exercise_name

    def preview(self, exercise_name: str, group_number: str):
        for group_correction in self._grades_service.get_exercise_feedback_by_name(
            exercise_name
        ):
            if group_correction.group.group_number == group_number:
                return self._email_service.preview_template_message(
                    self._message_from_correction(group_correction)
                )
                
        return "Non valid group number"
