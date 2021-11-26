from grades.domain.models.correction import GroupCorrection
from src.grades.application.grades_service import GradesService
from src.email.application.exercise_email import (
    ExerciseData,
    ExerciseEmail,
    ExerciseEmailData,
)


class ExercisesEmailView:
    def __init__(
        self, grades_service: GradesService, email_service: ExerciseEmail
    ) -> None:
        self._grades_service = grades_service
        self._email_service = email_service

    def _generate_exercises_data(self, group_correction: GroupCorrection):
        return ExerciseEmailData(
            student_emails=group_correction.group.emails,
            exercise_data=ExerciseData(
                exercise_name=group_correction.correction.activity_name,
                group_number=group_correction.group.group_number,
                corrector_name=group_correction.correction.corrector_name,
                correction_details=group_correction.correction.details,
                grade=group_correction.correction.grade,
            ),
        )

    def send(self, exercise_name: str):
        for group_correction in self._grades_service.get_exercise_feedback_by_name(
            exercise_name
        ):
            self._email_service.send_email(
                self._generate_exercises_data(group_correction)
            )

        return exercise_name

    def preview(self, exercise_name: str, group_number: str):
        for group_correction in self._grades_service.get_exercise_feedback_by_name(
            exercise_name
        ):
            if group_correction.group.group_number == group_number:
                return self._email_service.preview_template_message(
                    self._generate_exercises_data(group_correction)
                )

        return "Non valid group number"
