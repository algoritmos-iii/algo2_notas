import smtplib
import flask
from config import EmailConfig
from .abstract_mailable import AbstractMailable

email_config = EmailConfig()


def gmail_smtp_connection():
    connection = smtplib.SMTP_SSL(host="smtp.gmail.com", port=465)
    connection.login(user=email_config.account, password=email_config.password)

    return connection


def mailhog_smtp_connection():
    return smtplib.SMTP(host="localhost", port=1025)


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


"""
A variable to decide which smtp service to use.
* Use `mailhog_smtp_connection` for testing purposes
(first initialize mailhog)
* Use `gmail_smtp_connection` for production
"""
smtp_connection = mailhog_smtp_connection
