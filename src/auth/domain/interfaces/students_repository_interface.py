from typing import Optional, Protocol
from ..models.student import StudentSigninInfo


class StudentsRepositoryInterface(Protocol):
    """
    A Students Repository is in charge of getting the data of the students that
    have access to the app.
    """

    def get_student_by_padron(self, padron: str) -> Optional[StudentSigninInfo]:
        """Returns all the students by padron"""
        ...
