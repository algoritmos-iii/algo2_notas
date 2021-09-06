from __future__ import annotations

import gspread

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Tuple, List
    from gspread.models import Worksheet
    from api.google_credentials import GoogleCredentials

class NotasRepository:
    # Constantes
    SHEET_NOTAS: str = "Notas APP"
    SHEET_ALUMNOS: str = "Listado"

    COL_EMAIL: str = "E-Mail"
    COL_PADRON: str = "Padrón"

    def __init__(self, spreadsheet_key: str, credentials: GoogleCredentials) -> None:
        self._spreadsheet_key = spreadsheet_key
        self._google_credentials = credentials

    def _get_sheet(self, worksheet_name: str) -> Worksheet:
        """Devuelve un objeto gspread.Worksheet.
        Utiliza la constante global SPREADSHEET_KEY.
        """
        client = gspread.authorize(
            self._google_credentials.get_credenciales_spreadsheet())
        spreadsheet = client.open_by_key(self._spreadsheet_key)
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
        filas = notas.get_all_values()
        headers = filas.pop(0)
        idx_padron = headers.index(self.COL_PADRON)

        for alumno in filas:
            if padron.lower() == alumno[idx_padron].lower():
                return list(zip(headers, alumno))

        raise IndexError(f"Padrón {padron} no encontrado")
