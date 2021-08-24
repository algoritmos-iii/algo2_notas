#!/usr/bin/env python3

import os
import gspread

import notas_oauth

# Constantes
COL_EMAIL = "E-Mail"
COL_PADRON = "Padrón"

SHEET_NOTAS = "Notas APP"
SHEET_ALUMNOS = "Listado"

# Configuración externa.
SPREADSHEET_KEY = os.environ["NOTAS_SPREADSHEET_KEY"]


def get_sheet(worksheet_name):
    """Devuelve un objeto gspread.Worksheet.
    Utiliza la constante global SPREADSHEET_KEY.
    """
    client = gspread.authorize(notas_oauth.get_credenciales_spreadsheet())
    spreadsheet = client.open_by_key(SPREADSHEET_KEY)
    return spreadsheet.worksheet(worksheet_name)


def verificar(padron_web, email_web):
    """Verifica que hay un alumno con el padrón y e-mail indicados.
    """
    alumnos = get_sheet(SHEET_ALUMNOS)
    
    for alumno in alumnos.get_all_records():
        email = alumno.get(COL_EMAIL, "").strip()
        padron = str(alumno.get(COL_PADRON, ""))

        if not email or not padron:
            continue

        if (padron.lower() == padron_web.lower() and
            email.lower() == email_web.lower()):
            return True

    return False

def notas(padron):
    notas = get_sheet(SHEET_NOTAS)
    filas = notas.get_all_values()
    headers = filas.pop(0)
    idx_padron = headers.index(COL_PADRON)

    for alumno in filas:
        if padron.lower() == alumno[idx_padron].lower():
            return zip(headers, alumno)

    raise IndexError("Padrón {} no encontrado".format(padron))


if __name__ == "__main__":
    print(verificar("942039", "aaa"))