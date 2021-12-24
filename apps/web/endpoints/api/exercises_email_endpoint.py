from src.grades.domain.models.correction import GroupCorrection
from src.grades.application.grades_service import GradesService
from src.emails.application.exercise_email import (
    ExerciseData,
    ExerciseEmailBuilder,
)
from src.emails.domain.interfaces.email_sender_interface import (
    EmailSenderInterface,
)


class ExercisesEmailView:
    def __init__(
        self,
        grades_service: GradesService,
        exercise_email_builder: ExerciseEmailBuilder,
        email_sender: EmailSenderInterface,
    ) -> None:
        self._grades_service = grades_service
        self._exercise_email_builder = exercise_email_builder
        self._email_sender = email_sender

    def _generate_exercises_data(self, group_correction: GroupCorrection):
        return ExerciseData(
            group_number=group_correction.group.group_number,
            exercise_name=group_correction.correction.activity_name,
            corrector_name=group_correction.correction.corrector_name,
            correction_details=group_correction.correction.details,
            grade=group_correction.correction.grade,
        )

    def send(self, exercise_name: str):
        emails = [
            self._exercise_email_builder.create_email(
                to_addr=correction.group.emails,
                exercise_email_data=self._generate_exercises_data(correction),
            )
            for correction in self._grades_service.get_not_sent_exercise_feedback(
                exercise_name
            )
        ]

        # TODO: add try catch for errors in email sending
        self._email_sender.send_multiple(emails)

        return exercise_name

    def preview(self, exercise_name: str, group_number: str):
        for group_correction in self._grades_service.get_exercise_feedback(
            exercise_name
        ):
            if group_correction.group.group_number == group_number:
                exercise_data = self._generate_exercises_data(group_correction)
                return self._exercise_email_builder.html_part(exercise_data)

        return "Not a valid group number"
