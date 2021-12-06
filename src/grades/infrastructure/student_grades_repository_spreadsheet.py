from __future__ import annotations
from typing import TYPE_CHECKING

from ...shared.infrastructure.spreadsheet_repository_base import (
    SpreadsheetRepositoryBase,
    spreadsheet_raw_data_to_dict,
)

from ..domain.interfaces.student_repository_interface import StudentRepositoryInterface
from ..domain.models.student import Grade, StudentInfo, StudentWithGrades

if TYPE_CHECKING:
    from typing import List, Optional


class StudentGradesRepositorySpreadsheet(
    StudentRepositoryInterface, SpreadsheetRepositoryBase
):
    WORKSHEET_NAME: str = "Alumnos - Notas"
    STUDENT_DATA_RANGE = "datos_estudiantes"
    EXERCISES_RANGE = "notas_ejercicios"
    EXAMS_RANGE = "notas_examenes"

    def __init__(self, service_account_credentials: dict, spreadsheet_key: str) -> None:
        super().__init__(service_account_credentials, spreadsheet_key)

        self._worksheet = self._get_worksheet(self.WORKSHEET_NAME)

    def get_all(self) -> List[StudentWithGrades]:
        (
            students_data_raw,
            exercises_data_raw,
            exams_data_raw,
        ) = self._worksheet.batch_get(
            [self.STUDENT_DATA_RANGE, self.EXERCISES_RANGE, self.EXAMS_RANGE],
            major_dimension="COLUMNS",
        )

        students = spreadsheet_raw_data_to_dict(students_data_raw)
        exercises = spreadsheet_raw_data_to_dict(exercises_data_raw)
        exams = spreadsheet_raw_data_to_dict(exams_data_raw)

        return [
            StudentWithGrades(
                student_info=StudentInfo(
                    email=student["Email"],
                    full_name=student["Nombre"],
                    padron=student["Padrón"],
                    group_number=student["Grupo"],
                ),
                exercises_grades=[
                    Grade(
                        activity_name=activity_name,
                        grade=float(grade.replace(",", ".")),
                    )
                    for activity_name, grade in exercises[student_idx].items()
                    if grade.strip() != ""
                ],
                exams_grades=[
                    Grade(
                        activity_name=activity_name,
                        grade=float(grade.replace(",", ".")),
                    )
                    for activity_name, grade in exams[student_idx].items()
                    if grade.strip() != ""
                ],
            )
            for student_idx, student in enumerate(students)
            if not student["Padrón"] == ""
        ]

    def get_student_by_padron(self, padron: str) -> Optional[StudentWithGrades]:
        students = self.get_all()

        try:
            return next(
                filter(lambda student: student.student_info.padron == padron, students)
            )
        except StopIteration:
            return None
