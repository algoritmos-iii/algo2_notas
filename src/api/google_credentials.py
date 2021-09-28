from __future__ import annotations

import datetime
import httplib2

import oauth2client.client
import google.oauth2.service_account
import google.auth.transport.requests

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from google.oauth2.credentials import Credentials
    from typing import Callable, Dict


class GoogleCredentials:
    # TODO: Unificar autenticacion para planilla y cuenta de mail.
    # Por ahora no encontramos la forma de enviar mails usando la service account.
    # Mantenemos por un lado el service account para acceder a la planilla y el client id/secret para enviar mails.
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
              "https://www.googleapis.com/auth/gmail.send"]

    # TODO: ACCESS_TOKEN deberia ser una variable o una constante?
    ACCESS_TOKEN = ""
    # TODO: TOKEN_EXPIRY deberia ser una variable o una constante?
    TOKEN_EXPIRY = datetime.datetime(2015, 1, 1)
    TOKEN_URI = "https://accounts.google.com/o/oauth2/token"
    USER_AGENT = "notasweb/1.0"

    def __init__(self, service_account_data: Dict[str, str], client_id: str, client_secret: str, oauth_refresh_token: str) -> None:
        self._credentials_spreadhseet = google.oauth2.service_account.Credentials.from_service_account_info(
            service_account_data,
            scopes=self.SCOPES
        )

        self._credentials_email = oauth2client.client.OAuth2Credentials(
            self.ACCESS_TOKEN,
            client_id, client_secret,
            oauth_refresh_token,
            self.TOKEN_EXPIRY,
            self.TOKEN_URI,
            self.USER_AGENT
        )

    def _get_credenciales(self,
                          creds: Credentials,
                          es_valida: Callable[[Credentials], bool],
                          refrescar: Callable[[Credentials], None]) -> Credentials:
        if not es_valida(creds):
            refrescar(creds)
        return creds

    def get_credenciales_spreadsheet(self) -> Credentials:
        """Devuelve nuestro objeto OAuth2Credentials para acceder a la planilla, actualizado.
        Esta función llama a _refresh() si el token expira en menos de 5 minutos.
        """
        return self._get_credenciales(
            self._credentials_spreadhseet,
            lambda creds: creds.valid,
            lambda creds: creds.refresh(
                google.auth.transport.requests.Request())
        )

    def get_credenciales_email(self) -> Credentials:
        """Devuelve nuestro objeto OAuth2Credentials para acceder al mail, actualizado.
        Esta función llama a _refresh() si el token expira en menos de 5 minutos.
        """
        return self._get_credenciales(
            self._credentials_email,
            lambda creds: creds.token_expiry -
            datetime.timedelta(minutes=5) > datetime.datetime.utcnow(),
            lambda creds: creds.refresh(httplib2.Http())
        )
