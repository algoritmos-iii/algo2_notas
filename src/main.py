#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import flask
import json
import itsdangerous
import dotenv
import time

from webargs import fields
from webargs.flaskparser import use_args

from .forms.authentication_form import AuthenticationForm

from .api.google_credentials import GoogleCredentials
from .repositories.notas_repository import NotasRepository, NotasRepositoryConfig
from .services.sendmail import EmailSender, SendmailException
from .security import WebAdminAuthentication

dotenv.load_dotenv()

# App configuration
APP_TITLE = f'{os.environ["NOTAS_COURSE_NAME"]} - Consulta de Notas'
SECRET_KEY = os.environ["NOTAS_SECRET"]
TEMPLATES_DIR = "../templates"

# Notas
SPREADSHEET_KEY = os.environ["NOTAS_SPREADSHEET_KEY"]

# Google credentials
CLIENT_ID = os.environ["NOTAS_OAUTH_CLIENT"]
CLIENT_SECRET = os.environ["NOTAS_OAUTH_SECRET"]
OAUTH_REFRESH = os.environ["NOTAS_REFRESH_TOKEN"]
SERVICE_ACCOUNT_CREDENTIALS = os.environ["NOTAS_SERVICE_ACCOUNT_CREDENTIALS"]

# Email
COURSE = os.environ['NOTAS_COURSE_NAME']
ACCOUNT = os.environ['NOTAS_ACCOUNT']

# Admin things
ADMIN_USERNAME = os.environ['ADMIN_USERNAME']
ADMIN_PASSWORD = os.environ['ADMIN_PASSWORD']

# Notas repository config
SHEET_ALUMNOS: str = "Listado"
COL_EMAIL: str = "E-Mail"
COL_PADRON: str = "Padrón"

SHEET_NOTAS: str = "Alumnos - Notas"
RANGO_NOTAS: str = "1:26"

SHEET_DEVOLUCIONES: str = "Devoluciones"
PREFIJO_RANGO_DEVOLUCIONES: str = "emails"
RANGO_EMAILS: str = "emailsGrupos"


# Inicialización de objetos
signer = itsdangerous.URLSafeSerializer(SECRET_KEY)

app = flask.Flask(__name__)
app.secret_key = SECRET_KEY
app.config.title = APP_TITLE
app.template_folder = TEMPLATES_DIR
jinja2_env: flask.templating.Environment = app.jinja_env

admin_auth = WebAdminAuthentication(
    admin_username=ADMIN_USERNAME,
    admin_password=ADMIN_PASSWORD
)

service_account_credentials_info = json.loads(SERVICE_ACCOUNT_CREDENTIALS)
google_credentials = GoogleCredentials(
    service_account_data=service_account_credentials_info,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    oauth_refresh_token=OAUTH_REFRESH
)

notas = NotasRepository(
    config=NotasRepositoryConfig(
        sheet_alumnos=SHEET_ALUMNOS,
        col_email=COL_EMAIL,
        col_padron=COL_PADRON,
        sheet_notas=SHEET_NOTAS,
        rango_notas=RANGO_NOTAS,
        sheet_devoluciones=SHEET_DEVOLUCIONES,
        prefijo_rango_devoluciones=PREFIJO_RANGO_DEVOLUCIONES,
        rango_emails=RANGO_EMAILS
    ),
    spreadsheet_key=SPREADSHEET_KEY,
    credentials=google_credentials
)

email_sender = EmailSender(
    jinja2_env=jinja2_env,
    google_credentials=google_credentials,
    from_name=COURSE,
    from_email=ACCOUNT
)


# Endpoints

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
                email_sender.send_mail(
                    template_path="emails/sign_in.html",
                    subject="Enlace para consultar las notas", to_addr=email,
                    curso=COURSE, enlace=genlink(padron))
            except SendmailException as exception:
                return flask.render_template("error.html", message=str(exception))
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
    except IndexError as exception:
        return flask.render_template("error.html", message=str(exception))
    else:
        return flask.render_template("result.html", items=notas_alumno)


@app.route("/send-grades", methods=['POST'])
@admin_auth.auth_required
def send_grades_endpoint():
    ejercicio = flask.request.args.get("ejercicio")
    if ejercicio == None:
        # TODO: improve
        return 'error'

    # Posibles errores
    # gspread.exceptions.WorksheetNotFound
    # gspread.exceptions.APIError ({'code': 400, 'message': "Unable to parse range:  {WORKSHEET}!{CELL_RANGE}", 'status': 'INVALID_ARGUMENT'})

    def generator():
        for grupo in notas.ejercicios(ejercicio):
            result = {
                "grupo": grupo.numero,
                "emails": grupo.emails,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
            }

            try:
                email_sender.send_mail(
                    template_path="emails/notas_ejercicio.html",
                    subject=f"Correccion de notas ejercicio {ejercicio} - Grupo {grupo.numero}", to_addr=grupo.emails,
                    curso=COURSE, ejercicio=ejercicio,
                    grupo=grupo.numero, corrector=grupo.corrector,
                    nota=grupo.nota, correcciones=grupo.detalle)
            except SendmailException as exception:
                result = {
                    **result,
                    "message_sent": False,
                    "error": str(exception)
                }
            else:
                result = {
                    **result,
                    "message_sent": True,
                    "error": None
                }
            finally:
                grupo.mark_email_sent("TRUE" if result["message_sent"] else "")
                yield json.dumps(result) + "\n"

    return app.response_class(generator(), mimetype="text/plain")

@app.route("/logout")
@admin_auth.logout_endpoint
def admin_logout():
    return flask.jsonify("Admin logged out")


def genlink(padron: str) -> str:
    """Devuelve el enlace de consulta para un padrón.
    """
    signed_padron: str = signer.dumps(padron)
    return flask.url_for("consultar", clave=signed_padron, _external=True)


if __name__ == "__main__":
    app.run(debug=True)
