import flask
from flask.views import MethodView
from ..forms.authentication_form import AuthenticationForm

from src.auth.domain.message_sender_interface import MessageSenderInterface
from src.auth.application.student_auth_service import StudentAuthService


class SigninView(MethodView):
    def __init__(self, student_auth_service: StudentAuthService, email_sender: MessageSenderInterface) -> None:
        self._form = AuthenticationForm()
        self._student_auth_service = student_auth_service
        self._email_sender = email_sender

    def get(self):
        # TODO change wip.html for index.html when is ready for PROD
        return flask.render_template("index.html", form=self._form)

    def post(self):
        self._form.validate()
        email_address = self._form.normalized_email()
        padron = self._form.normalized_padron()

        student = self._student_auth_service.find_student(
            email_address, padron)

        if not student:
            flask.flash(
                "La dirección de mail no está asociada a ese padrón", "danger")
            return self.get()

        student_login_url = flask.url_for(
            "grades", key="{signed_padron}", _external=True)

        try:
            self._student_auth_service.send_login_message(student, student_login_url)
        except Exception as exception:
            return flask.render_template("error.html", message=str(exception))
        else:
            return flask.render_template("email_sent.html", email=student.email)
