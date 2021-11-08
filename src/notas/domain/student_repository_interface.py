from abc import ABC, abstractmethod
from typing import List, Optional

from .student import Student


class StudentRepositoryInterface(ABC):
    @abstractmethod
    def get_all(self) -> List[Student]:
        ...

    @abstractmethod
    def get_student_by_padron(self, padron: int) -> Optional[Student]:
        ...
