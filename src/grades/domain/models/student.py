from dataclasses import dataclass
from typing import List


@dataclass
class Grade:
    activity_name: str
    grade: float


@dataclass
class StudentInfo:
    """Represents the information about a student"""

    full_name: str
    email: str
    padron: str
    group_number: str


@dataclass
class StudentWithGrades:
    student_info: StudentInfo
    exercises_grades: List[Grade]
    exams_grades: List[Grade]
