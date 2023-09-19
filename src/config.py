from typing import Any
import json
import os


class BaseConfig:
    def __init__(self) -> None:
        self.config = os.environ

    def _get_config_variable(self, name: str, default: Any = None):
        config = self.config.get(name, default)
        if config:
            return config.strip()
        return config


class EmailConfig(BaseConfig):
    @property
    def account(self) -> str:
        return self._get_config_variable("EMAIL_ACCOUNT")

    @property
    def password(self) -> str:
        return self._get_config_variable("EMAIL_PASSWORD")

    @property
    def docentes_email(self) -> str:
        return self._get_config_variable("EMAIL_DOCENTES")

    @property
    def smtp_server_address(self) -> str:
        return self._get_config_variable("EMAIL_SMTP_ADDRESS")

    @property
    def smtp_server_port(self) -> str:
        return self._get_config_variable("EMAIL_SMTP_PORT")

    @property
    def use_ssl(self) -> bool:
        return self._get_config_variable("EMAIL_USE_SSL").lower() == "true"


class SpreadsheetConfig(BaseConfig):
    @property
    def credentials(self) -> dict:
        return json.loads(self._get_config_variable("SPREADSHEET_CREDENTIALS"))

    @property
    def spreadsheet_key(self) -> str:
        return self._get_config_variable("SPREADSHEET_KEY")
