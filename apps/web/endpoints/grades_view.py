from typing import Optional
import flask
from flask.views import MethodView
from webargs import fields, ValidationError
from webargs.flaskparser import parser

from src.shared.domain.signer_interface import SignerInterface, BadData

class GradesView(MethodView):
    argmap = {"key": fields.Str(required=True)}

    def __init__(self, signer: SignerInterface) -> None:
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
        items = []
        return flask.render_template("result.html", items=items)