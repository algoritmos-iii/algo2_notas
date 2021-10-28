from __future__ import annotations
import gspread
import gspread.utils
from itertools import zip_longest

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Iterable, Tuple, List, TypedDict, Dict, Callable
    from gspread.models import Worksheet
    from ..api.google_credentials import GoogleCredentials


class FeedbackSpreadsheetData(TypedDict):
    data: Dict[str, Any]
    email_sent_row: int
    sheet: Worksheet


class DevolucionBase(TypedDict):
    corrector: str
    nota: str
    detalle: str
    mark_email_sent: Callable[[str], None]


class DevolucionDeGrupo(DevolucionBase):
    numero: str
    emails: List[str]


class DevolucionDeExamen(DevolucionBase):
    email: str


class NotasRepository:

    SHEET_ALUMNOS: str = "Listado"
    COL_EMAIL: str = "E-Mail"
    COL_PADRON: str = "Padrón"

    SHEET_NOTAS: str = "Alumnos - Notas"
    RANGO_NOTAS: str = "1:26"

    SHEET_DEVOLUCIONES: str = "Devoluciones"
    PREFIJO_RANGO_DEVOLUCIONES: str = "emails"
    RANGO_EMAILS: str = "emails_grupos"

    def __init__(self, spreadsheet_key: str, credentials: GoogleCredentials) -> None:
        self._spreadsheet_key = spreadsheet_key
        self._google_credentials = credentials

    def _get_spreadsheet(self):
        client = gspread.authorize(
            self._google_credentials.get_credenciales_spreadsheet()
        )
        spreadsheet = client.open_by_key(self._spreadsheet_key)
        return spreadsheet

    def _get_sheet(self, worksheet_name: str) -> Worksheet:
        """Devuelve un objeto gspread.Worksheet.
        Utiliza la constante global SPREADSHEET_KEY.
        """
        spreadsheet = self._get_spreadsheet()
        return spreadsheet.worksheet(worksheet_name)

    def verificar(self, padron_web: str, email_web: str) -> bool:
        """Verifica que hay un alumno con el padrón y e-mail indicados."""
        alumnos = self._get_sheet(self.SHEET_ALUMNOS)

        for alumno in alumnos.get_all_records():
            email = alumno.get(self.COL_EMAIL, "").strip()
            padron = str(alumno.get(self.COL_PADRON, ""))

            if not email or not padron:
                continue

            if (
                padron.lower() == padron_web.lower()
                and email.lower() == email_web.lower()
            ):
                return True

        return False

    def notas(self, padron: str) -> List[Tuple[str, str]]:
        notas = self._get_sheet(self.SHEET_NOTAS)
        filas = notas.get_values(self.RANGO_NOTAS, major_dimension="COLUMNS")
        headers = filas.pop(0)
        idx_padron = headers.index(self.COL_PADRON)

        for alumno in filas:
            if padron.lower() == alumno[idx_padron].lower():
                return list(zip(headers, alumno))

        raise IndexError(f"Padrón {padron} no encontrado")

    def _exercise_name_to_named_range(self, exercise: str):
        """
        Convierte el nombre del ejercicio al nombre del named range.
        Ej: `"Codigo Repetido" -> "emails_codigo_repetido"`
        """
        words = exercise.strip().split(" ")
        words_lowercased = [word.lower() for word in words]
        spreadsheet_exercise_name = "_".join(words_lowercased)
        named_range_name = (
            f"{self.PREFIJO_RANGO_DEVOLUCIONES}_{spreadsheet_exercise_name}"
        )
        return named_range_name

    def _table_to_dict(self, table: Iterable):
        """
        Receives a list of lists where the first element is the Headers of the table
        and the rest are the data.
        Returns a tuple with the headers and a dict with data and the headers.
        """
        headers = table.pop(0)
        data = [dict(zip_longest(headers, element, fillvalue="")) for element in table]
        return data

    def _get_feedback_data(self, hoja: str, ejercicio: str) -> FeedbackSpreadsheetData:
        exercise_named_range = self._exercise_name_to_named_range(ejercicio)

        sheet = self._get_sheet(hoja)
        batch = sheet.batch_get(
            ranges=[f"{self.RANGO_EMAILS}", exercise_named_range],
            major_dimension="COLUMNS",
        )

        data = [{**self._table_to_dict(elem1), **self._table_to_dict(elem2)} for elem1, elem2 in zip(batch[0], batch[1])]

        correciones_range = batch[1].range.split("!")[1]
        # email_sent_row is zero indexed
        email_sent_row = gspread.utils.a1_range_to_grid_range(correciones_range)[
            "endRowIndex"
        ]

        return {"data": data, "email_sent_row": email_sent_row, "sheet": sheet}

    def _mark_email_sent_wrapper(
        self, sheet: Worksheet, row: int, col: int
    ) -> Callable[[str], None]:
        return lambda value: sheet.update_cell(row=row, col=col + 1, value=value)

    def _filter_field_not_empty(
        fields_which_cant_be_empty: Iterable[str],
    ) -> Callable[[Dict[str, Any]], bool]:
        EMPTY_CHARS_SET = {"#N/A", "#¡REF!", "", "0"}

        def _filter_criteria(elem: Dict[str, Any]):
            fields_contents = set(elem[field] for field in fields_which_cant_be_empty)
            return any(EMPTY_CHARS_SET.intersection(fields_contents))

        return _filter_criteria

    def examenes(self, examen: str) -> List[DevolucionDeExamen]:
        filter_func = self._filter_field_not_empty({"Email", "Corrector", "Detalle"})

        feedback = self._get_feedback_data(
            hoja=self.SHEET_DEVOLUCIONES, ejercicio=examen
        )

        grupos: List[DevolucionDeGrupo] = [
            {
                "emails": grupo["Email"],
                "corrector": grupo["Corrector"],
                "detalle": grupo["Detalle"],
                "nota": grupo["Nota"],
                "mark_email_sent": self._mark_email_sent_wrapper(
                    sheet=feedback["sheet"], row=feedback["email_sent_row"], col=index
                ),
            }
            for index, grupo in enumerate(filter(filter_func, feedback["data"]))
        ]

        return grupos

    def ejercicios(self, ejercicio: str) -> List[DevolucionDeGrupo]:
        filter_func = self._filter_field_not_empty(
            {"Grupo", "Email", "Corrector", "Detalle"}
        )
        feedback = self._get_feedback_data(
            hoja=self.SHEET_DEVOLUCIONES, ejercicio=ejercicio
        )

        grupos: List[DevolucionDeGrupo] = [
            {
                "numero": grupo["Grupo"],
                "emails": [email.strip() for email in grupo["Emails"].split(",")],
                "corrector": grupo["Corrector"],
                "detalle": grupo["Detalle"],
                "nota": grupo["Nota"],
                "mark_email_sent": self._mark_email_sent_wrapper(
                    sheet=feedback["sheet"], row=feedback["email_sent_row"], col=index
                ),
            }
            for index, grupo in enumerate(filter(filter_func, feedback["data"]))
        ]

        return grupos
