import smtplib
from jinja2 import Environment
from config import EmailConfig
from .abstract_mailable import AbstractMailable


def smtp_connection(
    server_address: str,
    server_port: int,
    account: str | None = None,
    password: str | None = None,
    use_ssl: bool = False,
):
    SMTPConnection = smtplib.SMTP_SSL if use_ssl else smtplib.SMTP
    connection = SMTPConnection(host=server_address, port=server_port)
    if account and password:
        connection.login(user=account, password=password)

    return connection


class Email(AbstractMailable):
    def __init__(self, env: Environment) -> None:
        super().__init__()
        self._env = env

    def _render_template(self, template_name: str, context: dict):
        return self._env.get_template(template_name).render(context)

    def set_plaintext_content_from_template(self, template_name: str, context: dict):
        return self.set_plaintext_content(self._render_template(template_name, context))

    def set_html_content_from_template(self, template_name: str, context: dict):
        return self.set_html_content(self._render_template(template_name, context))