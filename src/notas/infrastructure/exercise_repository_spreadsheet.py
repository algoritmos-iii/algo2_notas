from __future__ import annotations
from typing import TYPE_CHECKING

from .spreadsheet_repository_base import (
    SpreadsheetRepositoryBase,
    spreadsheet_raw_data_to_dict,
)
from ..domain.exercises_repository_interface import ExerciseRepositoryInterface
from ..domain.correction import (
    GroupCorrectionCollection,
    GroupCorrection,
    Correction,
    GroupSendingInformation,
)

if TYPE_CHECKING:
    from typing import List, Optional


def _string_to_snake_case(string: str) -> str:
    return string.lower().replace(" ", "_")


def _exercise_to_named_range(exercise_name: str) -> str:
    return "emails_" + _string_to_snake_case(exercise_name)


class ExerciseRepositorySpreadsheet(
    ExerciseRepositoryInterface, SpreadsheetRepositoryBase
):

    WORKSHEET_NAME: str = "Devoluciones"
    EMAIL_RANGE: str = "emailsGrupos"

    EXERCISES = [
        "NPCs",
        "Codigo Repetido",
        "Números",
        "Stack",
        "Mars Rover",
        "Servicios Financieros",
        "Servicios Financieros 2",
    ]

    def __init__(self, service_account_credentials: dict, spreadsheet_key: str) -> None:
        super().__init__(service_account_credentials, spreadsheet_key)

        self._worksheet = self._get_worksheet(self.WORKSHEET_NAME)

    def get(self) -> List[GroupCorrectionCollection]:
        ranges = [self.EMAIL_RANGE] + [
            _exercise_to_named_range(exercise) for exercise in self.EXERCISES
        ]
        emails_raw, *correcciones_raw = self._worksheet.batch_get(
            ranges, major_dimension="COLUMNS"
        )

        emails = spreadsheet_raw_data_to_dict(emails_raw)
        corrections = [
            spreadsheet_raw_data_to_dict(correccion_raw)
            for correccion_raw in correcciones_raw
        ]

        return [
            GroupCorrectionCollection(
                group=GroupSendingInformation(
                    group_number=emails[group_idx]["Grupo"],
                    emails=emails[group_idx]["Emails"].split(","),
                ),
                corrections=[
                    Correction(
                        exercise_name=self.EXERCISES[correction_idx],
                        grade=corrections[correction_idx][group_idx]["Nota"],
                        corrector_name=corrections[correction_idx][group_idx][
                            "Corrector"
                        ],
                        details=corrections[correction_idx][group_idx]["Detalle"],
                    )
                    for correction_idx in range(len(corrections))
                ],
            )
            for group_idx in range(len(emails))
            if not emails[group_idx]["Emails"] == ""
        ]

    def find(self, exercise_name: str) -> Optional[GroupCorrection]:
        exercise_range = _exercise_to_named_range(exercise_name)
        emails_raw, correcciones_raw = self._worksheet.batch_get(
            [self.EMAIL_RANGE, exercise_range], major_dimension="COLUMNS"
        )

        emails = spreadsheet_raw_data_to_dict(emails_raw)
        correcciones = spreadsheet_raw_data_to_dict(correcciones_raw)

        return [
            GroupCorrection(
                group=GroupSendingInformation(
                    group_number=email["Grupo"],
                    emails=email["Emails"].split(","),
                ),
                correction=Correction(
                    exercise_name=exercise_name,
                    grade=correccion["Nota"],
                    corrector_name=correccion["Corrector"],
                    details=correccion["Detalle"],
                ),
            )
            for email, correccion in zip(emails, correcciones)
            if not email["Emails"] == ""
        ]
