from abc import ABC, abstractmethod
from typing import List, Optional

from .correction import GroupCorrectionCollection, GroupCorrection


class ExerciseRepositoryInterface(ABC):
    @abstractmethod
    def get(self) -> List[GroupCorrectionCollection]:
        ...

    @abstractmethod
    def find(self, exercise_name: str) -> Optional[GroupCorrection]:
        ...
