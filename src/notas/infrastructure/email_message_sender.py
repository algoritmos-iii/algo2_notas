import smtplib
import jinja2

from .email import Email
from ..domain.messages.base_message import BaseMessage
from ..domain.messages.login_message import LoginMessage
from ..domain.student import StudentInfo


class EmailMessageSender:
    from_addr = "Algoritmos3Leveroni <fiuba.algoritmos.iii@gmail.com>"
    docentes_email = "Docentes Algoritmos 3 <fiuba.algoritmos.iii.doc@gmail.com>"

    def __init__(
        self,
        gmail_username: str,
        gmail_password: str,
        templater: jinja2.Environment,
    ) -> None:
        self._gmail_username = gmail_username
        self._gmail_password = gmail_password
        self._templater = templater

    def _create_login_email(self, message: LoginMessage):
        plain_template = self._templater.get_template("emails/sign_in_plain.html")
        html_template = self._templater.get_template("emails/sign_in.html")
        email = Email(
            subject="Enlace para consultar las notas",
            reply_to=self.docentes_email,
        )
        email.add_plaintext_content(plain_template.render(enlace=message.login_link))
        email.add_html_content(html_template.render(enlace=message.login_link))
        return email

    def _create_email(self, student: StudentInfo, message: BaseMessage):
        if type(message) is LoginMessage:
            return self._create_login_email(message)
        raise Exception("Message type not recognized")

    def send(self, student: StudentInfo, message: BaseMessage):
        email = self._create_email(student, message)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(self._gmail_username, self._gmail_password)
            server.send_message(
                msg=email.message,
                from_addr=self.from_addr,
                to_addrs=student.email,
            )
