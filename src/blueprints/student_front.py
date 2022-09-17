import flask
import itsdangerous
from config import AppConfig
from forms.authentication_form import AuthenticationForm
from emails import smtp_connection, Email
from db import (
    get_exam_by_padron_and_name,
    get_student_by_padron,
    get_exercises_by_group,
    get_exams_by_padron,
    get_exercise_by_group_and_name,
)

config = AppConfig()
signer = itsdangerous.URLSafeSerializer(config.secret_key)

student_front_blueprint = flask.Blueprint(
    name="student_front",
    import_name=__name__,
    template_folder="templates",
)


def create_login_email(url, email):
    context = {"enlace": url}
    return (
        Email()
        .set_subject("Enlace para consultar las notas")
        .set_recipients(email)
        .set_plaintext_content_from_template("emails/sign_in_plain.html", context)
        .set_html_content_from_template("emails/sign_in.html", context)
    )


def user_is_valid(padron: str, email: str) -> bool:
    candidate = get_student_by_padron(padron)
    print(candidate)
    return candidate != None and candidate["email"] == email


@student_front_blueprint.route("/", methods=["GET", "POST"])
def index():
    auth_form = AuthenticationForm()

    if auth_form.validate_on_submit():
        student_padron = auth_form.normalized_padron()
        student_email = auth_form.normalized_email()

        if user_is_valid(student_padron, student_email):
            key = signer.dumps(student_padron)
            url = flask.request.url + flask.url_for(".notas", key=key)

            email = create_login_email(url, student_email)

            # TODO: put try-except for errors
            with smtp_connection() as connection:
                connection.send_message(email.generate_email_message())

            return flask.render_template("email_sent.html", email=student_email)
        else:
            flask.flash("La dirección de mail no está asociada a ese padrón", "danger")

    return flask.render_template("index.html", form=auth_form)


@student_front_blueprint.get("/grades")
def notas():
    encoded_key = flask.request.args.get("key", None)

    if encoded_key is None:
        return flask.redirect(flask.url_for(".index"))

    try:
        padron = signer.loads(encoded_key)
    except itsdangerous.BadData:
        return flask.render_template(
            "error.html",
            msg="Ha ocurrido un error. Por favor, intentá iniciar sesion nuevamente.",
        )

    # Get data from padron
    student = get_student_by_padron(padron)
    exercises = get_exercises_by_group(student["grupo"])
    exams = get_exams_by_padron(student["padron"])

    return flask.render_template(
        "grades.html",
        student_name=student["nombre"],
        student_group=student["grupo"],
        student_email=student["email"],
        student_padron=student["padron"],
        exercises=exercises,
        exams=exams,
        encoded_key=encoded_key,
    )


@student_front_blueprint.get("/grades/exercises/<exercise>")
def exercise_detail(exercise: str):
    encoded_key = flask.request.args.get("key", None)

    if encoded_key is None:
        return flask.redirect(flask.url_for(".index"))

    try:
        padron = signer.loads(encoded_key)
    except itsdangerous.BadData:
        return flask.render_template(
            "error.html",
            msg="Ha ocurrido un error. Por favor, intentá iniciar sesion nuevamente.",
        )

    student = get_student_by_padron(padron)
    exercise_data = get_exercise_by_group_and_name(student["grupo"], exercise)

    return flask.render_template(
        "emails/notas_ejercicio.html",
        ejercicio=exercise_data["title"],
        grupo=exercise_data["grupo"],
        corrector=exercise_data["corrector"],
        nota=exercise_data["nota"],
        correcciones=exercise_data["detalle"],
    )


@student_front_blueprint.get("/grades/exams/<exam>")
def exam_detail(exam: str):
    encoded_key = flask.request.args.get("key", None)

    if encoded_key is None:
        return flask.redirect(flask.url_for(".index"))

    try:
        padron = signer.loads(encoded_key)
    except itsdangerous.BadData:
        return flask.render_template(
            "error.html",
            msg="Ha ocurrido un error. Por favor, intentá iniciar sesion nuevamente.",
        )

    student = get_student_by_padron(padron)
    exam_data = get_exam_by_padron_and_name(padron, exam)

    return flask.render_template(
        "emails/notas_ejercicio.html",
        nombre=student["nombre"],
        examen=exam_data["title"],
        corrector=exam_data["corrector"],
        correcciones=exam_data["detalle"],
        nota=exam_data["nota"],
        puntos_extras=exam_data["puntos_extra"],
        nota_final=exam_data["nota_final"],
    )
