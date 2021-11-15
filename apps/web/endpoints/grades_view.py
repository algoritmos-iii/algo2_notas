from typing import Optional
import flask
from flask.views import MethodView
from webargs import fields
from webargs.flaskparser import parser

from src.grades.application.grades_service import GradesService
from src.shared.domain.signer_interface import SignerInterface, BadData

class GradesView(MethodView):
    argmap = {"key": fields.Str(required=True)}

    def __init__(self, grades_service: GradesService, signer: SignerInterface) -> None:
        self._grades_service = grades_service
        self._signer = signer

    def _validate_signed_padron(self, signed_padron: str) -> Optional[str]:
        try:
            return self._signer.unsign(signed_padron)
        except BadData:
            return None

    def get(self):
        args = parser.parse(self.argmap)
        padron = self._validate_signed_padron(args['key'])
        if not padron:
            return flask.render_template("error.html", message="El link utilizado es inválido. Por favor, intente nuevamente.")

        # padron is valid at this point
        student = self._grades_service.get_student_with_grades_by_padron(padron)
        if not student:
            return flask.render_template("error.html", message="El link utilizado es inválido. Por favor, intente nuevamente.")

        return flask.render_template("grades.html", student=student)