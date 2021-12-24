from dataclasses import dataclass
from typing import List


@dataclass
class Correction:
    activity_name: str
    corrector_name: str
    grade: float
    details: str
    email_has_been_sent: bool


@dataclass
class GroupSendingInformation:
    group_number: str
    emails: List[str]


@dataclass
class GroupCorrection:
    group: GroupSendingInformation
    correction: Correction


@dataclass
class IndividualSendingInformation:
    padron: str
    email: str
    full_name: str


@dataclass
class IndividualCorrection:
    individual: IndividualSendingInformation
    correction: Correction


@dataclass
class ExamCorrection:
    individual: IndividualSendingInformation
    correction: Correction
    exam_data: dict
