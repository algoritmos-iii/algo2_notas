from ..domain.interfaces.student_repository_interface import StudentRepositoryInterface
from ..domain.interfaces.feedback_repository_interface import (
    FeedbackRepositoryInterface,
)
from ...shared.domain.signer_interface import SignerInterface


class GradesService:
    def __init__(
        self,
        grades_repository: StudentRepositoryInterface,
        feedback_repository: FeedbackRepositoryInterface,
        signer: SignerInterface,
    ) -> None:
        self._grades_repository = grades_repository
        self._feedback_repository = feedback_repository
        self._signer = signer

    def get_student_with_grades_by_padron(self, padron: str):
        return self._grades_repository.get_student_by_padron(padron)

    def get_exercise_feedback_by_name(self, exercise_name: str):
        return self._feedback_repository.get_exercises_corrections_by_exercise_name(
            exercise_name
        )

    def get_exam_feedback_by_name(self, exam_name: str):
        return self._feedback_repository.get_exams_corrections_by_exam_name(exam_name)
