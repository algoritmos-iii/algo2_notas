from abc import ABC, abstractmethod
from typing import List, Optional

from student import Student


class StudentRepositoryInterface(ABC):

    @abstractmethod
    def list(self) -> List[Student]:
        ...

    @abstractmethod
    def find(self, padron: int) -> Optional[Student]:
        ...
