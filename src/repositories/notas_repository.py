from __future__ import annotations
import gspread
import gspread.utils

from typing import TYPE_CHECKING, Tuple
from dataclasses import dataclass, field

if TYPE_CHECKING:
    from typing import Tuple, List, Callable
    from gspread.models import Worksheet
    from ..api.google_credentials import GoogleCredentials


@dataclass(frozen=True)
class Grupo:
    numero: str
    emails: List[str]
    corrector: str = field(repr=False)
    nota: str = field(repr=False)
    detalle: str = field(repr=False)
    mark_email_sent: Callable[[str], None] = field(repr=False)


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
            self._google_credentials.get_credenciales_spreadsheet())
        spreadsheet = client.open_by_key(self._spreadsheet_key)
        return spreadsheet

    def _get_sheet(self, worksheet_name: str) -> Worksheet:
        """Devuelve un objeto gspread.Worksheet.
        Utiliza la constante global SPREADSHEET_KEY.
        """
        spreadsheet = self._get_spreadsheet()
        return spreadsheet.worksheet(worksheet_name)

    def verificar(self, padron_web: str, email_web: str) -> bool:
        """Verifica que hay un alumno con el padrón y e-mail indicados.
        """
        alumnos = self._get_sheet(self.SHEET_ALUMNOS)

        for alumno in alumnos.get_all_records():
            email = alumno.get(self.COL_EMAIL, "").strip()
            padron = str(alumno.get(self.COL_PADRON, ""))

            if not email or not padron:
                continue

            if (padron.lower() == padron_web.lower() and
                    email.lower() == email_web.lower()):
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
        named_range_name = f"{self.PREFIJO_RANGO_DEVOLUCIONES}_{spreadsheet_exercise_name}"
        return named_range_name
        

    def ejercicios(self, ejercicio: str) -> List[Grupo]:
        exercise_named_range = self._exercise_name_to_named_range(ejercicio)

        sheet = self._get_sheet(self.SHEET_DEVOLUCIONES)
        emails, correcciones = sheet.batch_get(
            [f"{self.RANGO_EMAILS}", exercise_named_range],
            major_dimension="COLUMNS")

        # Construct headers
        email_headers = emails.pop(0)
        correciones_headers = correcciones.pop(0)

        raw_data = [[
            *emails[i],
            *[""] * (len(email_headers) - len(emails[i])),
            *correcciones[i],
            *[""] * (
                (len(email_headers) + len(correciones_headers)) -
                (len(emails[i]) + len(correcciones[i]))
            )
        ] for i in range(len(correcciones))]

        correciones_range = correcciones.range.split("!")[1]
        # email_sent_row is zero indexed
        email_sent_row = gspread.utils.a1_range_to_grid_range(correciones_range)[
            'endRowIndex']

        grupos = []
        EMPTY_CHARS_FIELD = ["#N/A", "#¡REF!", "", "0"]
        for g in filter(lambda elem: elem[1] not in EMPTY_CHARS_FIELD and elem[5] in EMPTY_CHARS_FIELD, raw_data):
            func: Callable[[int], Callable[[str], None]] = (
                lambda group_number: (
                    lambda value="True": sheet.update_cell(
                        row=email_sent_row,
                        col=group_number + 1,
                        value=value
                    )
                )
            )

            grupos.append(
                Grupo(
                    numero=g[0],
                    emails=g[1].split(","),
                    nota=g[2],
                    corrector=g[3],
                    detalle=g[4],
                    mark_email_sent=func(int(g[0]))
                )
            )

        return grupos
