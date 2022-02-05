import flask
import itsdangerous
from config import AppConfig
from spreadsheet_data_mapper.data_mapper import DataMapper
from forms.authentication_form import AuthenticationForm
from emails import smtp_connection, Email

config = AppConfig()
data_mapper = DataMapper()
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
        .set_cc(None)
        .set_plaintext_content_from_template("emails/sign_in_plain.html", context)
        .set_html_content_from_template("emails/sign_in.html", context)
    )


def user_is_valid(padron: str, email: str) -> bool:
    candidate = data_mapper.student_by_padron(padron)
    return candidate != None and candidate.email == email


def get_student_data(padron: str):
    student = data_mapper.student_by_padron(padron)
    student_group = data_mapper.group_of_student(student.padron)
    exercises = data_mapper.exercises_feedback_by_group_number(
        student_group.group_number
    )
    exams = data_mapper.exams_feedback_by_student(student.padron)

    return student, student_group, exercises, exams


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

    if encoded_key == None:
        return flask.redirect(flask.url_for(".index"))

    try:
        key = signer.loads(encoded_key)
    except itsdangerous.BadData:
        return flask.render_template(
            "error.html",
            msg="Ha ocurrido un error. Por favor, intentá iniciar sesion nuevamente.",
        )

    # Get data from padron
    student, student_group, exercises, exams = get_student_data(padron=key)

    return flask.render_template(
        "grades.html",
        student_name=student.full_name,
        student_group=student_group.group_number,
        student_email=student.email,
        student_padron=student.padron,
        exercises=exercises,
        exams=exams,
    )
