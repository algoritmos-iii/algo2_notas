from abc import ABC, abstractmethod
from typing import List, Optional

from ..models.student import StudentWithGrades


class StudentRepositoryInterface(ABC):
    @abstractmethod
    def get_all(self) -> List[StudentWithGrades]:
        ...

    @abstractmethod
    def get_student_by_padron(self, padron: str) -> Optional[StudentWithGrades]:
        ...
