from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING

import gspread
import gspread.utils

if TYPE_CHECKING:
    from gspread import Worksheet
    from typing import List
    from gspread.models import ValueRange

def spreadsheet_raw_data_to_dict(raw_data: ValueRange) -> List:
    values: List[str] = gspread.utils.fill_gaps(raw_data)
    keys = values.pop(0)

    return [dict(zip(keys, row)) for row in values]

class SpreadsheetRepositoryBase(ABC):
    """
    Abstract class from which all repositories that use a spreadsheet as a
    storage mechanism can inherit from.
    """

    def __init__(self, spreadsheet_credentials, spreadsheet_key: str) -> None:
        self._spreadhseet_credentials = spreadsheet_credentials
        self._spreadhseet_key = spreadsheet_key

    def _get_worksheet(self, worksheet_name: str) -> Worksheet:
        client = gspread.authorize(self._spreadhseet_credentials)
        spreadsheet = client.open_by_key(self._spreadsheet_key)
        return spreadsheet.worksheet(worksheet_name)