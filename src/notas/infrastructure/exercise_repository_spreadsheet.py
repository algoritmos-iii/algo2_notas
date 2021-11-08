from __future__ import annotations
from typing import TYPE_CHECKING

from .spreadsheet_repository_base import SpreadsheetRepositoryBase, spreadsheet_raw_data_to_dict
from ..domain.exercises_repository_interface import ExerciseRepositoryInterface
from ..domain.correction import GroupCorrection, Correction

if TYPE_CHECKING:
    from typing import List, Optional


def _string_to_snake_case(string: str) -> str:
    return string.lower().replace(' ', '_')


def _exercise_to_named_range(exercise_name: str) -> str:
    return 'emails_' + _string_to_snake_case(exercise_name)


class ExerciseRepositorySpreadsheet(SpreadsheetRepositoryBase, ExerciseRepositoryInterface):

    WORKSHEET_NAME: str = "Devoluciones"

    def __init__(self, spreadsheet_credentials, spreadsheet_key: str) -> None:
        super().__init__(spreadsheet_credentials, spreadsheet_key)

        self._worksheet = self._get_worksheet(self.WORKSHEET_NAME)

    def list(self) -> List[GroupCorrection]:
        ...

    def find(self, exercise_name: str) -> Optional[GroupCorrection]:
        exercise_range = _exercise_to_named_range(exercise_name)
        emails_raw, correcciones_raw = self._worksheet.batch_get(
            [f"{self.RANGO_EMAILS}", exercise_range],
            major_dimension="COLUMNS"
        )

        emails = spreadsheet_raw_data_to_dict(emails_raw)
        correcciones = spreadsheet_raw_data_to_dict(correcciones_raw)

        return [
            GroupCorrection(
                group_number=email['Grupo'],
                emails=email['Emails'],
                correction=Correction(
                    exercise_name=exercise_name,
                    grade=correccion['Nota'],
                    corrector_name=correccion['Corrector'],
                    details=correccion['Detalle'],
                )
            )
            for email, correccion in zip(emails, correcciones)
        ]
