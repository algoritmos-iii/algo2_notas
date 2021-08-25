#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import flask
import flask_wtf
import itsdangerous

from webargs import fields as wfields
from webargs.flaskparser import use_args

from wtforms import fields
from wtforms import validators
from wtforms.fields import html5

import notas
import sendmail

app = flask.Flask(__name__)
app.secret_key = os.environ["NOTAS_SECRET"]
app.config.title = os.environ["NOTAS_COURSE_NAME"] + " - Consulta de Notas"

assert app.secret_key
signer = itsdangerous.URLSafeSerializer(app.secret_key)


class Formulario(flask_wtf.FlaskForm):
    """Pide el padrón y la dirección de correo.
    """
    padron = fields.StringField(
        "Ingresa tu padrón", validators=[
            validators.Regexp(r"\w+", message="Ingrese un padrón válido")])

    email = html5.EmailField(
        "Ingresa tu e-mail", validators=[
            validators.Email(message="Ingrese una dirección de e-mail válida")])

    submit = fields.SubmitField("Obtener enlace")


@app.route("/", methods=('GET', 'POST'))
def index():
    """Sirve la página de solicitud del enlace.
    """
    form = Formulario()

    if form.validate_on_submit():
        padron = norm_field(form.padron)
        email = norm_field(form.email).strip()

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


def validate(value):
    # Needed because URLSafeSerializer does not have a validate().
    try:
        return bool(signer.loads(value))
    except itsdangerous.BadSignature:
        return False


@app.route("/consultar")
@use_args({"clave": wfields.Str(required=True, validate=validate)})
def consultar(args):
    try:
        notas_alumno = notas.notas(signer.loads(args["clave"]))
    except IndexError as e:
        return flask.render_template("error.html", message=str(e))
    else:
        return flask.render_template("result.html", items=notas_alumno)


def norm_field(f):
    """Devuelve los datos del campo en minúsculas y sin espacio alreadedor.
    """
    return f.data.strip().lower()


def genlink(padron):
    """Devuelve el enlace de consulta para un padrón.
    """
    signed_padron = signer.dumps(padron)
    return flask.url_for("consultar", clave=signed_padron, _external=True)


if __name__ == "__main__":
    app.run(debug=True)
