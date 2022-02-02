import flask
import itsdangerous
from config import AppConfig
from spreadsheet_data_mapper.data_mapper import DataMapper
from forms.authentication_form import AuthenticationForm

config = AppConfig()
data_mapper = DataMapper()
signer = itsdangerous.URLSafeSerializer(config.secret_key)

student_front_blueprint = flask.Blueprint(
    "student_front", __name__, template_folder="templates"
)


def send_login_email(url, email):
    print(f"Email para {email}")
    print(f"Tu url es {url}")


def user_is_valid(padron: str, email: str) -> bool:
    candidate = data_mapper.student_by_padron(padron)
    return candidate != None and candidate.email == email


@student_front_blueprint.route("/", methods=["GET", "POST"])
def index():
    auth_form = AuthenticationForm()

    if auth_form.validate_on_submit():
        padron = auth_form.normalized_padron()
        email = auth_form.normalized_email()

        if user_is_valid(padron, email):
            key = signer.dumps(padron)
            url = flask.request.url + flask.url_for(".notas", key=key)

            send_login_email(url=url, email=email)
            return flask.render_template("email_sent.html", email=email)
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
    padron = key

    student = data_mapper.student_by_padron(padron)
    student_group = data_mapper.get_group_of_student(student.padron)
    exercises = data_mapper.exercises_feedback_by_group_number(
        student_group.group_number
    )
    exams = data_mapper.exams_feedback_by_student(student.padron)

    return flask.render_template(
        "grades.html",
        student_name=student.full_name,
        student_group=student_group.group_number,
        student_email=student.email,
        student_padron=student.padron,
        exercises=exercises,
        exams=exams,
    )
