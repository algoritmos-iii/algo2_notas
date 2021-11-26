import flask
from flask.views import MethodView


from ..forms.authentication_form import AuthenticationForm

from src.auth.application.student_auth_service import StudentAuthService
from src.email.domain.models.message import TemplateMessage
from src.shared.domain.signer_interface import SignerInterface

from src.email.application.login_email import LoginData, LoginEmail, LoginEmailData


class SigninView(MethodView):
    def __init__(
        self,
        student_auth_service: StudentAuthService,
        signin_email_service: LoginEmail,
        signer: SignerInterface,
    ) -> None:
        self._form = AuthenticationForm()
        self._student_auth_service = student_auth_service
        self._signin_email_service = signin_email_service
        self._signer = signer

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

        try:
            self._signin_email_service.send_email(
                LoginEmailData(
                    student_email=student.email,
                    login_data=LoginData(student_login_url),
                )
            )
        # TODO: replace exception for a more specific
        except Exception as exception:
            return flask.render_template("error.html", message=str(exception))
        else:
            return flask.render_template("email_sent.html", email=student.email)
