from dataclasses import dataclass
from typing import List


@dataclass
class Correction:
    exercise_name: str
    corrector_name: str
    grade: str
    details: str


@dataclass
class GroupSendingInformation:
    group_number: int
    emails: List[str]


@dataclass
class GroupCorrectionCollection:
    group: GroupSendingInformation
    corrections: List[Correction]


@dataclass
class GroupCorrection:
    group: GroupSendingInformation
    correction: Correction
