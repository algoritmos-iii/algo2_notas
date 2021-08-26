# -*- coding: utf-8 -*-

"""Módulo para autenticación con OAuth2."""

import datetime
import httplib2
import os

import oauth2client.client
import google.oauth2.service_account
import google.auth.transport.requests

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Callable
    from google.oauth2.service_account import Credentials


CLIENT_ID = os.environ["NOTAS_OAUTH_CLIENT"]
CLIENT_SECRET = os.environ["NOTAS_OAUTH_SECRET"]
OAUTH_REFRESH = os.environ["NOTAS_REFRESH_TOKEN"]
SERVICE_ACCOUNT_JSON = os.environ["NOTAS_SERVICE_ACCOUNT_JSON"]

SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
           "https://www.googleapis.com/auth/gmail.send"]

# TODO: Unificar autenticacion para planilla y cuenta de mail.
# Por ahora no encontramos la forma de enviar mails usando la service account.
# Mantenemos por un lado el service account para acceder a la planilla y el client id/secret para enviar mails.
_creds_spreadhseet = google.oauth2.service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_JSON, scopes=SCOPES)
_creds_email = oauth2client.client.OAuth2Credentials(
    "", CLIENT_ID, CLIENT_SECRET, OAUTH_REFRESH,
    datetime.datetime(2015, 1, 1),
    "https://accounts.google.com/o/oauth2/token", "notasweb/1.0")


def _get_credenciales(creds: Credentials,
                      es_valida: Callable[[Credentials], bool],
                      refrescar: Callable[[Credentials], None]) -> Credentials:
    if not es_valida(creds):
        refrescar(creds)
    return creds


def get_credenciales_spreadsheet() -> Credentials:
    """Devuelve nuestro objeto OAuth2Credentials para acceder a la planilla, actualizado.
    Esta función llama a _refresh() si el token expira en menos de 5 minutos.
    """
    return _get_credenciales(
        _creds_spreadhseet,
        lambda creds: creds.valid,
        lambda creds: creds.refresh(google.auth.transport.requests.Request())
    )


def get_credenciales_email() -> Credentials:
    """Devuelve nuestro objeto OAuth2Credentials para acceder al mail, actualizado.
    Esta función llama a _refresh() si el token expira en menos de 5 minutos.
    """
    return _get_credenciales(
        _creds_email,
        lambda creds: creds.token_expiry -
        datetime.timedelta(minutes=5) > datetime.datetime.utcnow(),
        lambda creds: creds.refresh(httplib2.Http())
    )
