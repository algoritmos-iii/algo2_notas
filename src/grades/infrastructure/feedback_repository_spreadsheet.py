from __future__ import annotations
from typing import TYPE_CHECKING

from ..domain.interfaces.feedback_repository_interface import (
    FeedbackRepositoryInterface,
)
from ..domain.models.correction import (
    Correction,
    ExamCorrection,
    GroupCorrection,
    GroupSendingInformation,
    IndividualCorrection,
    IndividualSendingInformation,
)
from ...shared.infrastructure.spreadsheet_repository_base import (
    SpreadsheetRepositoryBase,
    spreadsheet_raw_data_to_dict,
)

if TYPE_CHECKING:
    from gspread.models import Worksheet
    from typing import List


def _string_to_snake_case(string: str) -> str:
    return string.lower().replace(" ", "_")


def exercise_to_named_range(exercise_name: str) -> str:
    return "emails_" + _string_to_snake_case(exercise_name)


def exam_to_named_range(exam_name: str) -> str:
    return "emails_examen_" + _string_to_snake_case(exam_name)


class FeedbackRepositorySpreadsheet(
    FeedbackRepositoryInterface, SpreadsheetRepositoryBase
):

    EXERCISES_WORKSHEET_NAME: str = "Devoluciones"
    EXERCISES_EMAIL_RANGE: str = "emailsGrupos"

    EXAMS_WORKSHEET_NAME: str = "Devoluciones examenes"
    EXAMS_EMAIL_RANGE: str = "emails_individuos"

    def __init__(self, service_account_credentials: dict, spreadsheet_key: str) -> None:
        super().__init__(service_account_credentials, spreadsheet_key)

        self._exercises_worksheet = self._get_worksheet(self.EXERCISES_WORKSHEET_NAME)
        self._exams_worksheet = self._get_worksheet(self.EXAMS_WORKSHEET_NAME)

    def _get_feedback(
        self, worksheet: Worksheet, email_range_name: str, activity_named_range: str
    ) -> tuple[List, List]:
        emails_raw, corrections_raw = worksheet.batch_get(
            [email_range_name, activity_named_range],
            major_dimension="COLUMNS",
        )

        emails = spreadsheet_raw_data_to_dict(emails_raw)
        corrections = spreadsheet_raw_data_to_dict(corrections_raw)

        return emails, corrections

    def get_exercises_corrections_by_exercise_name(
        self, exercise_name: str
    ) -> List[GroupCorrection]:
        emails, corrections = self._get_feedback(
            self._exercises_worksheet,
            self.EXERCISES_EMAIL_RANGE,
            exercise_to_named_range(exercise_name),
        )

        return [
            GroupCorrection(
                group=GroupSendingInformation(
                    group_number=email["Grupo"],
                    emails=email["Emails"].split(","),
                ),
                correction=Correction(
                    activity_name=exercise_name,
                    grade=float(correction["Nota"].replace(",", ".")),
                    corrector_name=correction["Corrector"],
                    details=correction["Detalle"],
                ),
            )
            for email, correction in zip(emails, corrections)
            if not email["Emails"] == ""
        ]

    def get_exams_corrections_by_exam_name(
        self, exam_name: str
    ) -> List[IndividualCorrection]:
        emails, corrections = self._get_feedback(
            self._exams_worksheet,
            self.EXAMS_EMAIL_RANGE,
            exam_to_named_range(exam_name),
        )

        return [
            ExamCorrection(
                individual=IndividualSendingInformation(
                    padron=email["Padrón"],
                    email=email["Email"],
                    full_name=email["Nombre"],
                ),
                correction=Correction(
                    activity_name=exam_name,
                    grade=float(correction["Nota"].replace(",", ".")),
                    corrector_name=correction["Corrector"],
                    details=correction["Detalle"],
                ),
                exam_data={
                    "extra_points": float(correction["Puntos extra"].replace(",", ".")),
                    "final_grade": float(correction["Nota final"].replace(",", ".")),
                },
            )
            for email, correction in zip(emails, corrections)
            if (not email["Email"] == "") and (not correction["EMAIL_SENT"])
        ]
