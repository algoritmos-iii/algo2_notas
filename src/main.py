#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import flask
import itsdangerous

from webargs import fields
from webargs.flaskparser import use_args

from forms.authentication_form import AuthenticationForm
import notas

APP_TITLE = os.environ["NOTAS_COURSE_NAME"] + " - Consulta de Notas"
SECRET_KEY = os.environ["NOTAS_SECRET"]
assert SECRET_KEY
TEMPLATES_DIR = "../templates"

signer = itsdangerous.URLSafeSerializer(SECRET_KEY)

app = flask.Flask(__name__)
app.secret_key = SECRET_KEY
app.config.title = APP_TITLE
app.template_folder = TEMPLATES_DIR

@app.route("/", methods=('GET', 'POST'))
def index():
    """Sirve la página de solicitud del enlace.
    """
    form = AuthenticationForm()

    if form.validate_on_submit():
        padron = form.padron_normalizado()
        email = form.email_normalizado()

        if not notas.verificar(padron, email):
            flask.flash(
                "La dirección de mail no está asociada a ese padrón", "danger")
        else:
            try:
                notas_alumno = notas.notas(padron)
            except IndexError as e:
                return flask.render_template("error.html", message=str(e))
            else:
                return flask.render_template("result.html", items=notas_alumno)

    return flask.render_template("index.html", form=form)


@app.errorhandler(422)
def bad_request(err):
    """Se invoca cuando falla la validación de la clave.
    """
    return flask.render_template("error.html", message="Clave no válida")


def _clave_validate(clave) -> bool:
    # Needed because URLSafeSerializer does not have a validate().
    try:
        return bool(signer.loads(clave))
    except itsdangerous.BadSignature:
        return False


@app.route("/consultar")
@use_args({"clave": fields.Str(required=True, validate=_clave_validate)})
def consultar(args):
    try:
        notas_alumno = notas.notas(signer.loads(args["clave"]))
    except IndexError as e:
        return flask.render_template("error.html", message=str(e))
    else:
        return flask.render_template("result.html", items=notas_alumno)

# def genlink(padron: str) -> str:
#     """Devuelve el enlace de consulta para un padrón.
#     """
#     signed_padron = signer.dumps(padron)
#     return flask.url_for("consultar", clave=signed_padron, _external=True)


if __name__ == "__main__":
    app.run(debug=True)
