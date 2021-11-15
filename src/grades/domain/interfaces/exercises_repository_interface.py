from abc import ABC, abstractmethod
from typing import List, Optional

from ..models.correction import GroupCorrectionCollection, GroupCorrection


class ExerciseRepositoryInterface(ABC):
    @abstractmethod
    def get_all(self) -> List[GroupCorrectionCollection]:
        ...

    @abstractmethod
    def get_corrections_by_exercise(self, exercise_name: str) -> List[GroupCorrection]:
        ...

    @abstractmethod
    def get_corrections_by_group(self, group_number: int) -> Optional[GroupCorrectionCollection]:
        ...
