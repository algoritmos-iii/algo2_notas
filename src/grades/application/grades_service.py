from typing import Optional

from ..domain.models.student import StudentWithGrades
from ..domain.interfaces.student_repository_interface import StudentRepositoryInterface
from ...shared.domain.signer_interface import SignerInterface


class GradesService:
    def __init__(
        self,
        grades_repository: StudentRepositoryInterface,
        signer: SignerInterface,
    ) -> None:
        self._grades_repository = grades_repository
        self._signer = signer

    def get_student_with_grades_by_padron(self, padron: str) -> Optional[StudentWithGrades]:
        return self._grades_repository.get_student_by_padron(padron)