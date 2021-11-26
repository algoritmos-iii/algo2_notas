import os
import json
import flask

from src.shared.infrastructure.itsdangerous_signer import ItsDangerousSigner

from src.email.infrastructure.mock_email_message_sender import MockEmailMessageSender
from src.email.infrastructure.email_message_sender import EmailMessageSender
from src.email.infrastructure.jinja2_templater import Jinja2Templater

# Email services
from src.email.application.login_email import LoginEmail
from src.email.application.exercise_email import ExerciseEmail
from src.email.application.exam_email import ExamEmail

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

# App config
SECRET_KEY: str = os.environ["NOTAS_SECRET"]

# Spreadhseet config
SERVICE_ACCOUNT_CREDENTIALS: str = json.loads(
    os.environ["NOTAS_SERVICE_ACCOUNT_CREDENTIALS"]
)
SPREADSHEET_KEY: str = os.environ["NOTAS_SPREADSHEET_KEY"]

# Gmail config
EMAIL_ACCOUNT: str = os.environ["EMAIL_ACCOUNT"]
EMAIL_PASSWORD: str = os.environ["EMAIL_PASSWORD"]
DOCENTES_EMAIL = '"Docentes Algoritmos 3" <fiuba-algoritmos-iii-doc@googlegroups.com>'

# Flask configuration
app = flask.Flask(__name__)
app.config["title"] = "Algoritmos 3 - Consulta de Notas"
app.secret_key = SECRET_KEY

# Signer
signer = ItsDangerousSigner(SECRET_KEY)

# Email
templater = Jinja2Templater("./apps/web/templates")
email_sender = EmailMessageSender(EMAIL_ACCOUNT, EMAIL_PASSWORD)
login_email = LoginEmail(email_sender, templater, DOCENTES_EMAIL)
exercise_email = ExerciseEmail(email_sender, templater, DOCENTES_EMAIL)
exam_email = ExamEmail(email_sender, templater, DOCENTES_EMAIL)

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
    signin_email_service=login_email,
    signer=signer,
)
grades_view = GradesView.as_view(
    name="grades",
    grades_service=grades_service,
    signer=signer,
)

exercises_email_view = ExercisesEmailView(
    grades_service=grades_service,
    email_service=exercise_email,
)
exams_email_view = ExamsEmailView(
    grades_service=grades_service,
    email_service=exam_email,
)

# Endpoints
app.add_url_rule("/", view_func=signin_view)
app.add_url_rule("/grades/", view_func=grades_view)
app.add_url_rule(
    "/api/emails/exercise/<exercise_name>/send",
    view_func=exercises_email_view.send,
)
app.add_url_rule(
    "/api/emails/exercise/<exercise_name>/preview/<group_number>",
    view_func=exercises_email_view.preview,
)

app.add_url_rule(
    "/api/emails/exam/<exam_name>/send",
    endpoint="send_email",
    view_func=exams_email_view.send,
)
app.add_url_rule(
    "/api/emails/exam/<exam_name>/preview/<padron_number>",
    endpoint="preview_email",
    view_func=exams_email_view.preview,
)
