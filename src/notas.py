#!/usr/bin/env python3

import os
import gspread

import notas_oauth

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Tuple, List
    from gspread.models import Worksheet

# Constantes
COL_EMAIL: str = "E-Mail"
COL_PADRON: str = "Padrón"

SHEET_NOTAS: str = "Notas APP"
SHEET_ALUMNOS: str = "Listado"

# Configuración externa.
SPREADSHEET_KEY: str = os.environ["NOTAS_SPREADSHEET_KEY"]


def _get_sheet(worksheet_name: str) -> Worksheet:
    """Devuelve un objeto gspread.Worksheet.
    Utiliza la constante global SPREADSHEET_KEY.
    """
    client = gspread.authorize(notas_oauth.get_credenciales_spreadsheet())
    spreadsheet = client.open_by_key(SPREADSHEET_KEY)
    return spreadsheet.worksheet(worksheet_name)


def verificar(padron_web: str, email_web: str) -> bool:
    """Verifica que hay un alumno con el padrón y e-mail indicados.
    """
    alumnos = _get_sheet(SHEET_ALUMNOS)

    for alumno in alumnos.get_all_records():
        email = alumno.get(COL_EMAIL, "").strip()
        padron = str(alumno.get(COL_PADRON, ""))

        if not email or not padron:
            continue

        if (padron.lower() == padron_web.lower() and
                email.lower() == email_web.lower()):
            return True

    return False


def notas(padron: str) -> List[Tuple[str, str]]:
    notas = _get_sheet(SHEET_NOTAS)
    filas = notas.get_all_values()
    headers = filas.pop(0)
    idx_padron = headers.index(COL_PADRON)

    for alumno in filas:
        if padron.lower() == alumno[idx_padron].lower():
            return list(zip(headers, alumno))

    raise IndexError(f"Padrón {padron} no encontrado")


if __name__ == "__main__":
    print(verificar("942039", "aaa"))
