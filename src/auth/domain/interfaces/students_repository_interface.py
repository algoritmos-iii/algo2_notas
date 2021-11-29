from typing import Optional, Protocol
from ..models.student import StudentSigninInfo


class StudentsRepositoryInterface(Protocol):
    def get_student_by_padron(self, padron: str) -> Optional[StudentSigninInfo]:
        ...
