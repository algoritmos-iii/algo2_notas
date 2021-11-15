from __future__ import annotations
from typing import TYPE_CHECKING

from ..domain.interfaces.exercises_repository_interface import ExerciseRepositoryInterface
from ..domain.models.correction import (
    GroupCorrectionCollection,
    GroupCorrection,
    Correction,
    GroupSendingInformation,
)
from ...shared.infrastructure.spreadsheet_repository_base import (
    SpreadsheetRepositoryBase,
    spreadsheet_raw_data_to_dict,
    exercise_to_named_range
)

if TYPE_CHECKING:
    from typing import List, Optional


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

    def get_all(self) -> List[GroupCorrectionCollection]:
        ranges = [self.EMAIL_RANGE] + [
            exercise_to_named_range(exercise) for exercise in self.EXERCISES
        ]
        emails_raw, *correcciones_raw = self._worksheet.batch_get(
            ranges,
            major_dimension="COLUMNS",
        )

        emails = spreadsheet_raw_data_to_dict(emails_raw)
        corrections = [
            spreadsheet_raw_data_to_dict(correccion_raw)
            for correccion_raw in correcciones_raw
        ]

        return [
            GroupCorrectionCollection(
                group=GroupSendingInformation(
                    group_number=int(emails[group_idx]["Grupo"]),
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

    def get_corrections_by_exercise(self, exercise_name: str) -> List[GroupCorrection]:
        exercise_range = exercise_to_named_range(exercise_name)
        emails_raw, corrections_raw = self._worksheet.batch_get(
            [self.EMAIL_RANGE, exercise_range], major_dimension="COLUMNS"
        )

        emails = spreadsheet_raw_data_to_dict(emails_raw)
        corrections = spreadsheet_raw_data_to_dict(corrections_raw)

        return [
            GroupCorrection(
                group=GroupSendingInformation(
                    group_number=int(email["Grupo"]),
                    emails=email["Emails"].split(","),
                ),
                correction=Correction(
                    exercise_name=exercise_name,
                    grade=correction["Nota"],
                    corrector_name=correction["Corrector"],
                    details=correction["Detalle"],
                ),
            )
            for email, correction in zip(emails, corrections)
            if not email["Emails"] == ""
        ]

    def get_corrections_by_group(
        self, group_number: int
    ) -> Optional[GroupCorrectionCollection]:
        all_corrections = self.get_all()

        try:
            return next(
                filter(
                    lambda group_correction: group_correction.group.group_number
                    == group_number,
                    all_corrections,
                )
            )
        except StopIteration:
            return None
