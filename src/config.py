from typing import Any
import json
import os
import dotenv

dotenv.load_dotenv(dotenv_path="../")

config = {
    "EMAIL_DOCENTES": "fiuba-algoritmos-iii-doc@googlegroups.com",
    "TEMPLATES_DIR": "../templates"
}


class BaseConfig:
    def __init__(self) -> None:
        self.config = config
        self.config = {**self.config, **os.environ}

    def get_config_variable(self, name: str, default: Any = None):
        return self.config.get(name, default)


class AppConfig(BaseConfig):
    @property
    def title(self) -> str:
        title = self.get_config_variable("NOTAS_COURSE_NAME")
        return f"{title} - Consulta de Notas"

    @property
    def secret_key(self) -> str:
        return self.get_config_variable("NOTAS_SECRET")

    @property
    def template_folder(self) -> str:
        return self.get_config_variable("TEMPLATES_DIR")

    @property
    def environment(self):
        return self.get_config_variable("ENVIRONMENT")


class AdminConfig(BaseConfig):
    @property
    def username(self) -> str:
        return self.get_config_variable("ADMIN_USERNAME")

    @property
    def password(self) -> str:
        return self.get_config_variable("ADMIN_PASSWORD")


class EmailConfig(BaseConfig):
    @property
    def account(self) -> str:
        return self.get_config_variable("EMAIL_ACCOUNT")

    @property
    def password(self) -> str:
        return self.get_config_variable("EMAIL_PASSWORD")

    @property
    def docentes_email(self) -> str:
        return self.get_config_variable("EMAIL_DOCENTES")


class SpreadsheetConfig(BaseConfig):
    @property
    def spreadsheet_auth_dict(self) -> dict:
        auth_data = self.get_config_variable("NOTAS_SERVICE_ACCOUNT_CREDENTIALS")
        return json.loads(auth_data)

    @property
    def spreadsheet_key(self) -> str:
        return self.get_config_variable("NOTAS_SPREADSHEET_KEY")
