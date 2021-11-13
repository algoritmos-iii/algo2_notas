from typing import Any, List, Tuple
from ...shared.domain.signer_interface import SignerInterface


class GradesService:
    def __init__(self, grades_repository, signer: SignerInterface) -> None:
        self._grades_repository = grades_repository
        self._signer = signer

    def get_student_grades(self) -> List[Tuple[str, Any]]:
        ...