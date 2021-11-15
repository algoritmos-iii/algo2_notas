import flask
from src.email.application.email_service import EmailService
from src.email.domain.models.message import TemplateMessage


class ExercisesEmailView:
    def __init__(self, email_service: EmailService) -> None:
        self._email_service = email_service

    def send(self, exercise_name: str):
        self._email_service.send_template_message(
            TemplateMessage(
                subject=f"Corrección de ejercicio {exercise_name}",
                to=...,
                template_name="notas_ejercicio",
                context={
                    "curso": ...,
                    "ejercicio": exercise_name,
                    "grupo": ...,
                    "corrector": ...,
                    "nota": ...,
                    "correcciones": ...,
                },
                with_copy_to_docentes=True,
            )
        )
        return exercise_name
