import flask
from flask.views import MethodView

from src.auth.application.student_auth_service import StudentAuthService
from src.shared.domain.signer_interface import SignerInterface

from src.emails.application.login_email_builder import LoginEmailBuilder
from src.emails.domain.interfaces.email_sender_interface import (
    EmailSenderInterface,
)

from ..forms.authentication_form import AuthenticationForm


class SigninView(MethodView):
    def __init__(
        self,
        student_auth_service: StudentAuthService,
        signer: SignerInterface,
        signin_email_builder: LoginEmailBuilder,
        email_sender: EmailSenderInterface,
    ) -> None:
        self._form = AuthenticationForm()
        self._student_auth_service = student_auth_service
        self._signer = signer

        self._signin_email_builder = signin_email_builder
        self._email_sender = email_sender

    def get(self):
        # TODO change wip.html for index.html when is ready for PROD
        return flask.render_template("index.html", form=self._form)

    def post(self):
        self._form.validate()
        email_address = self._form.normalized_email()
        padron = self._form.normalized_padron()

        student = self._student_auth_service.find_student(email_address, padron)
        if not student:
            flask.flash("La dirección de mail no está asociada a ese padrón", "danger")
            return self.get()

        student_login_url = flask.url_for(
            endpoint="grades",
            key=self._signer.sign(padron),
            _external=True,
        )

        email = self._signin_email_builder.create_email(
            to_addr=student.email,
            login_url=student_login_url,
        )

        try:
            self._email_sender.send(email)
        # TODO: replace exception for a more specific
        except Exception as exception:
            return flask.render_template("error.html", message=str(exception))
        else:
            return flask.render_template("email_sent.html", email=student.email)
