from __future__ import annotations

import google.oauth2.service_account
import google.auth.transport.requests

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from google.oauth2.credentials import Credentials
    from typing import Dict


class GoogleCredentials:
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

    def __init__(self, service_account_data: Dict[str, str]) -> None:
        self._credentials_spreadhseet = (
            google.oauth2.service_account.Credentials.from_service_account_info(
                service_account_data, scopes=self.SCOPES
            )
        )

    def get_credenciales_spreadsheet(self) -> Credentials:
        """Devuelve nuestro objeto OAuth2Credentials para acceder a la planilla, actualizado.
        Esta función llama a _refresh() si el token expira en menos de 5 minutos.
        """
        credentials = self._credentials_spreadhseet
        if not credentials:
            credentials.refresh(google.auth.transport.requests.Request())

        return credentials
