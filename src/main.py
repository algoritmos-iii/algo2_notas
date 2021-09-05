#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import flask
import itsdangerous

from webargs import fields
from webargs.flaskparser import use_args

from forms.authentication_form import AuthenticationForm

from api.google_credentials import GoogleCredentials
from repositories.notas_repository import NotasRepository
from services.sendmail import EmailSender

# App configuration
APP_TITLE = f'{os.environ["NOTAS_COURSE_NAME"]} - Consulta de Notas'
SECRET_KEY = os.environ["NOTAS_SECRET"]
assert SECRET_KEY
TEMPLATES_DIR = "../templates"

# Notas
SPREADSHEET_KEY = os.environ["NOTAS_SPREADSHEET_KEY"]

# Google credentials
CLIENT_ID = os.environ["NOTAS_OAUTH_CLIENT"]
CLIENT_SECRET = os.environ["NOTAS_OAUTH_SECRET"]
OAUTH_REFRESH = os.environ["NOTAS_REFRESH_TOKEN"]
SERVICE_ACCOUNT_JSON = os.environ["NOTAS_SERVICE_ACCOUNT_JSON"]

# Email
COURSE = os.environ['NOTAS_COURSE_NAME']
ACCOUNT = os.environ['NOTAS_ACCOUNT']

signer = itsdangerous.URLSafeSerializer(SECRET_KEY)

app = flask.Flask(__name__)
app.secret_key = SECRET_KEY
app.config.title = APP_TITLE
app.template_folder = TEMPLATES_DIR

google_credentials = GoogleCredentials(SERVICE_ACCOUNT_JSON, CLIENT_ID, CLIENT_SECRET, OAUTH_REFRESH)
notas = NotasRepository(SPREADSHEET_KEY, google_credentials)
emails = EmailSender(COURSE, ACCOUNT, google_credentials)

@app.route("/", methods=('GET', 'POST'))
def index():
    """Sirve la página de solicitud del enlace.
    """
    form = AuthenticationForm()

    if form.validate_on_submit():
        padron = form.normalized_padron()
        email = form.normalized_email()

        if not notas.verificar(padron, email):
            flask.flash(
                "La dirección de mail no está asociada a ese padrón", "danger")
        else:
            try:
                EmailSender.sendmail(emails, app.config.title, email, genlink(padron))
            except EmailSender.SendmailException as e:
                return flask.render_template("error.html", message=str(e))
            else:
                return flask.render_template("email_sent.html", email=email)

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

def genlink(padron: str) -> str:
    """Devuelve el enlace de consulta para un padrón.
    """
    signed_padron = signer.dumps(padron)
    return flask.url_for("consultar", clave=signed_padron, _external=True)


if __name__ == "__main__":
    app.run(debug=True)
