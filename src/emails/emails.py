import smtplib
import flask
from config import AppConfig, EmailConfig
from .abstract_mailable import AbstractMailable

app_config = AppConfig()
email_config = EmailConfig()

def smtp_connection():
    SMTPConnection = smtplib.SMTP_SSL if email_config.use_ssl else smtplib.SMTP
    connection = SMTPConnection(
        host=email_config.smtp_server_address,
        port=int(email_config.smtp_server_port),
    )
    if email_config.account:
        connection.login(user=email_config.account, password=email_config.password)

    return connection


class Email(AbstractMailable):
    def __init__(self) -> None:
        super().__init__()
        self.set_from(email_config.account)

    def set_plaintext_content_from_template(self, template_name: str, context: dict):
        return self.set_plaintext_content(
            flask.render_template(template_name, **context),
        )

    def set_html_content_from_template(self, template_name: str, context: dict):
        return self.set_html_content(
            flask.render_template(template_name, **context),
        )

    def set_cc_to_lista_docente(self, should_send_copy: bool):
        return self.set_cc(email_config.docentes_email if should_send_copy else None)
