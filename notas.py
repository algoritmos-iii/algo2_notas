#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import gspread

# Constantes
COL_EMAIL = "Email"
COL_PADRON = "Padrón"

SHEET_NOTAS = "Notas"
SHEET_ALUMNOS = "DatosAlumnos"

# Configuración externa.
ACCOUNT = os.environ["NOTAS_ACCOUNT"]
PASSWORD = os.environ["NOTAS_PASSWORD"]
SPREADSHEET_KEY = os.environ["NOTAS_SPREADSHEET_KEY"]


def get_sheet(worksheet_name):
    """Devuelve un objeto gspread.Worksheet.

    Utiliza la constante global SPREADSHEET_KEY.
    """
    # TODO: ClientLogin está deprecado. Usar gspread.authorize() instead.
    client = gspread.login(ACCOUNT, PASSWORD)
    spreadsheet = client.open_by_key(SPREADSHEET_KEY)
    return spreadsheet.worksheet(worksheet_name)


def verificar(padron_web, email_web):
    """Verifica que hay un alumno con el padrón y e-mail indicados.
    """
    alumnos = get_sheet(SHEET_ALUMNOS)

    for alumno in alumnos.get_all_records():
        email = alumno.get(COL_EMAIL, "")
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
        if padron == alumno[idx_padron]:
            return zip(headers, alumno)

    raise IndexError("Padrón %s no encontrado" % padron)


if __name__ == "__main__":
    print(verificar("942039", "aaa"))

