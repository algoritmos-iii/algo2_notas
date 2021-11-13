from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING

import gspread
import gspread.utils

if TYPE_CHECKING:
    from gspread import Worksheet
    from typing import List
    from gspread.models import ValueRange

# Helpers
def _string_to_snake_case(string: str) -> str:
    return string.lower().replace(" ", "_")


def exercise_to_named_range(exercise_name: str) -> str:
    return "emails_" + _string_to_snake_case(exercise_name)

def spreadsheet_raw_data_to_dict(raw_data: ValueRange) -> List:
    values: List[str] = gspread.utils.fill_gaps(raw_data)
    keys = values.pop(0)

    return [dict(zip(keys, row)) for row in values]


class SpreadsheetRepositoryBase(ABC):
    """
    Abstract class from which all repositories that use a spreadsheet as a
    storage mechanism can inherit from.
    """

    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

    def __init__(self, service_account_credentials: dict, spreadsheet_key: str) -> None:
        self._service_account_credentials = service_account_credentials
        self._spreadsheet_key = spreadsheet_key

    def _get_worksheet(self, worksheet_name: str) -> Worksheet:
        client = gspread.service_account_from_dict(
            info=self._service_account_credentials, scopes=self.SCOPES
        )
        spreadsheet = client.open_by_key(self._spreadsheet_key)
        return spreadsheet.worksheet(worksheet_name)
