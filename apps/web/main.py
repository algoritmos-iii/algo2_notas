import os
import json
import flask

from src.shared.infrastructure.itsdangerous_signer import ItsDangerousSigner

# Email things
from src.emails.infrastructure.mock_email_sender import MockEmailSender
from src.emails.infrastructure.email_sender import EmailSender
from src.emails.infrastructure.jinja2_templater import Jinja2Templater

# Email Builders
from src.emails.application.exam_email_builder import ExamEmailBuilder
from src.emails.application.exercise_email_builder import ExerciseEmailBuilder
from src.emails.application.login_email_builder import LoginEmailBuilder

# Spreadsheet repositories
from src.auth.infrastructure.students_repository import StudentRepository
from src.auth.application.student_auth_service import StudentAuthService

from src.grades.infrastructure.feedback_repository_spreadsheet import (
    FeedbackRepositorySpreadsheet,
)
from src.grades.infrastructure.student_grades_repository_spreadsheet import (
    StudentGradesRepositorySpreadsheet,
)
from src.grades.application.grades_service import GradesService

# Views imports
from apps.web.endpoints.signin_view import SigninView
from apps.web.endpoints.grades_view import GradesView
from apps.web.endpoints.api.exercises_email_endpoint import ExercisesEmailView
from apps.web.endpoints.api.exams_email_endpoint import ExamsEmailView

from apps.web.webauthentication import WebAdminAuthentication

# App config
SECRET_KEY: str = os.environ["NOTAS_SECRET"]
ADMIN_USERNAME: str = os.environ["ADMIN_USERNAME"]
ADMIN_PASSWORD: str = os.environ["ADMIN_PASSWORD"]

# Spreadhseet config
SERVICE_ACCOUNT_CREDENTIALS: str = json.loads(
    os.environ["NOTAS_SERVICE_ACCOUNT_CREDENTIALS"]
)
SPREADSHEET_KEY: str = os.environ["NOTAS_SPREADSHEET_KEY"]

# Gmail config
EMAIL_ACCOUNT: str = os.environ["EMAIL_ACCOUNT"]
EMAIL_PASSWORD: str = os.environ["EMAIL_PASSWORD"]
DOCENTES_EMAIL = "fiuba-algoritmos-iii-doc@googlegroups.com"

# Flask configuration
app = flask.Flask(__name__)
app.config["title"] = "Algoritmos 3 - Consulta de Notas"
app.secret_key = SECRET_KEY

# Web admin authentication
admin_authentication = WebAdminAuthentication(ADMIN_USERNAME, ADMIN_PASSWORD)

# Signer, templater and email sender
signer = ItsDangerousSigner(SECRET_KEY)
templater = Jinja2Templater("./apps/web/templates")
email_sender = EmailSender(EMAIL_ACCOUNT, EMAIL_PASSWORD)

# Email builders
exam_email_builder = ExamEmailBuilder(templater, EMAIL_ACCOUNT, DOCENTES_EMAIL)
exercise_email_builder = ExerciseEmailBuilder(templater, EMAIL_ACCOUNT, DOCENTES_EMAIL)
login_email_builder = LoginEmailBuilder(templater, EMAIL_ACCOUNT, DOCENTES_EMAIL)

# Students auth
student_repository = StudentRepository(
    service_account_credentials=SERVICE_ACCOUNT_CREDENTIALS,
    spreadsheet_key=SPREADSHEET_KEY,
)
student_auth_service = StudentAuthService(student_repository=student_repository)

# Students grades
grades_repository = StudentGradesRepositorySpreadsheet(
    service_account_credentials=SERVICE_ACCOUNT_CREDENTIALS,
    spreadsheet_key=SPREADSHEET_KEY,
)
feedback_repository = FeedbackRepositorySpreadsheet(
    service_account_credentials=SERVICE_ACCOUNT_CREDENTIALS,
    spreadsheet_key=SPREADSHEET_KEY,
)
grades_service = GradesService(
    grades_repository=grades_repository,
    feedback_repository=feedback_repository,
    signer=signer,
)


# Views
signin_view = SigninView.as_view(
    name="index",
    student_auth_service=student_auth_service,
    signer=signer,
    signin_email_builder=login_email_builder,
    email_sender=email_sender,
)

grades_view = GradesView.as_view(
    name="grades",
    grades_service=grades_service,
    signer=signer,
)

exercises_email_view = ExercisesEmailView(
    grades_service=grades_service,
    exercise_email_builder=exercise_email_builder,
    email_sender=email_sender,
)
exams_email_view = ExamsEmailView(
    grades_service=grades_service,
    exam_email_builder=exam_email_builder,
    email_sender=email_sender,
)

# Endpoints
app.add_url_rule("/", view_func=signin_view)
app.add_url_rule("/grades/", view_func=grades_view)

# API endpoints
app.add_url_rule(
    "/api/emails/exercise/<exercise_name>/send",
    view_func=admin_authentication.auth_required(exercises_email_view.send),
)
app.add_url_rule(
    "/api/emails/exercise/<exercise_name>/preview/<group_number>",
    view_func=admin_authentication.auth_required(exercises_email_view.preview),
)

app.add_url_rule(
    "/api/emails/exam/<exam_name>/send",
    endpoint="send_email",
    view_func=admin_authentication.auth_required(exams_email_view.send),
)
app.add_url_rule(
    "/api/emails/exam/<exam_name>/preview/<padron_number>",
    endpoint="preview_email",
    view_func=admin_authentication.auth_required(exams_email_view.preview),
)
