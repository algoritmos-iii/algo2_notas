from abc import ABC, abstractmethod
from typing import List, Optional

from .correction import GroupCorrection


class ExerciseRepositoryInterface(ABC):

    @abstractmethod
    def list(self) -> List[GroupCorrection]:
        ...

    @abstractmethod
    def find(self, exercise_name: str) -> Optional[GroupCorrection]:
        ...
