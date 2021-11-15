from abc import ABC, abstractmethod
from typing import List

from ..models.correction import (
    GroupCorrection,
    IndividualCorrection,
)


class FeedbackRepositoryInterface(ABC):
    @abstractmethod
    def get_exercises_corrections_by_exercise_name(
        self, exercise_name: str
    ) -> List[GroupCorrection]:
        ...

    @abstractmethod
    def get_exams_corrections_by_exam_name(
        self, exam_name: str
    ) -> List[IndividualCorrection]:
        ...
