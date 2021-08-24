# -*- coding: utf-8 -*-

"""Módulo para autenticación con OAuth2."""

import datetime
import httplib2
import os

import oauth2client.client
import google.oauth2.service_account
import google.auth.transport.requests

_CLIENT_ID = os.environ["NOTAS_OAUTH_CLIENT"]
_CLIENT_SECRET = os.environ["NOTAS_OAUTH_SECRET"]
_OAUTH_REFRESH = os.environ["NOTAS_REFRESH_TOKEN"]
_SERVICE_ACCOUNT_JSON = os.environ["NOTAS_SERVICE_ACCOUNT_JSON"]

SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/gmail.send"]

# TODO: Unificar autenticacion para planilla y cuenta de mail.
# Por ahora no encontramos la forma de enviar mails usando la service account.
# Mantenemos por un lado el service account para acceder a la planilla y el client id/secret para enviar mails.
_creds_spreadhseet = google.oauth2.service_account.Credentials.from_service_account_file(_SERVICE_ACCOUNT_JSON, scopes=SCOPES)
_creds_email = oauth2client.client.OAuth2Credentials(
    "", _CLIENT_ID, _CLIENT_SECRET, _OAUTH_REFRESH,
    datetime.datetime(2015, 1, 1),
    "https://accounts.google.com/o/oauth2/token", "notasweb/1.0")


def get_credenciales(creds, es_valida, refrescar):
    if not es_valida(creds):
        refrescar(creds)
    return creds


def get_credenciales_spreadsheet():
    """Devuelve nuestro objeto OAuth2Credentials para acceder a la planilla, actualizado.
    Esta función llama a _refresh() si el token expira en menos de 5 minutos.
    """
    return get_credenciales(
        _creds_spreadhseet,
        lambda creds: creds.valid,
        lambda creds: creds.refresh(google.auth.transport.requests.Request())
    )

def get_credenciales_email():
    """Devuelve nuestro objeto OAuth2Credentials para acceder al mail, actualizado.
    Esta función llama a _refresh() si el token expira en menos de 5 minutos.
    """
    return get_credenciales(
        _creds_email,
        lambda creds: creds.token_expiry - datetime.timedelta(minutes=5) > datetime.datetime.utcnow(),
        lambda creds: creds.refresh(httplib2.Http())
    )
