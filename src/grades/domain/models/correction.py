from dataclasses import dataclass
from typing import List


@dataclass
class Correction:
    activity_name: str
    corrector_name: str
    grade: str
    details: str


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


# @dataclass
# class GroupCorrectionCollection:
#     group: GroupSendingInformation
#     corrections: List[Correction]