from __future__ import annotations
from typing import TYPE_CHECKING

from .spreadsheet_repository_base import (
    SpreadsheetRepositoryBase,
)

from ..domain.student_repository_interface import StudentRepositoryInterface
from ..domain.student import Student

if TYPE_CHECKING:
    from typing import List, Optional


class StudentRepositorySpreadsheet(
    StudentRepositoryInterface, SpreadsheetRepositoryBase
):
    WORKSHEET_NAME: str = "Listado"

    def __init__(self, service_account_credentials: dict, spreadsheet_key: str) -> None:
        super().__init__(service_account_credentials, spreadsheet_key)

        self._worksheet = self._get_worksheet(self.WORKSHEET_NAME)

    def get_all(self) -> List[Student]:
        students = self._worksheet.get_all_records()

        return [
            Student(
                padron=int(student["Padrón"]),
                full_name=student["Nombre"],
                email=student["E-Mail"],
                group_number=int(student["Grupo"]),
            )
            for student in students
        ]

    def get_student_by_padron(self, padron: int) -> Optional[Student]:
        students = self.get_all()

        try:
            return next(filter(lambda student: student.padron == padron, students))
        except StopIteration:
            return None
