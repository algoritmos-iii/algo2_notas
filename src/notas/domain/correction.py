from dataclasses import dataclass
from typing import List


@dataclass
class Correction:
    exercise_name: str
    corrector_name: str
    grade: float
    details: str


@dataclass
class GroupCorrection:
    group_number: int
    emails: List[str]
    correction: Correction