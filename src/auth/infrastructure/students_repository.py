from typing import Optional
from ..domain.models.student import StudentSigninInfo
from ...shared.infrastructure.spreadsheet_repository_base import (
    SpreadsheetRepositoryBase,
    spreadsheet_raw_data_to_dict,
)


class StudentRepository(SpreadsheetRepositoryBase):
    def __init__(self, service_account_credentials: dict, spreadsheet_key: str) -> None:
        super().__init__(service_account_credentials, spreadsheet_key)
        self._sheet = self._get_worksheet("Alumnos - Notas")

    def get_student_by_padron(self, padron: str) -> Optional[StudentSigninInfo]:
        students_raw = self._sheet.get_values(
            "datos_estudiantes",
            major_dimension="COLUMNS",
        )
        students = spreadsheet_raw_data_to_dict(students_raw)

        for student in students:
            if student["Padrón"] == padron:
                return StudentSigninInfo(
                    email=student["Email"],
                    padron=padron,
                )

        return None
