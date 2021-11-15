from typing import Optional

from ..domain.models.student import StudentSigninInfo
from ..domain.interfaces.students_repository_interface import (
    StudentsRepositoryInterface,
)

class StudentAuthService:
    def __init__(self, student_repository: StudentsRepositoryInterface) -> None:
        self._student_repository = student_repository

    def find_student(self, email: str, padron: int) -> Optional[StudentSigninInfo]:
        student = self._student_repository.get_student_by_padron(padron)
        if (not student) or (student.email != email):
            return None

        return student
