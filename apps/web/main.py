import os
import json
import flask

from src.shared.infrastructure.itsdangerous_signer import ItsDangerousSigner
from src.auth.infrastructure.email_message_sender import EmailMessageSender
from src.auth.infrastructure.student_repository_spreadsheet import (
    StudentRepositorySpreadsheet,
)
from src.auth.application.student_auth_service import StudentAuthService

from src.grades.infrastructure.exercise_repository_spreadsheet import ExerciseRepositorySpreadsheet
from src.grades.application.grades_service import GradesService

# Views imports
from apps.web.endpoints.signin_view import SigninView
from apps.web.endpoints.grades_view import GradesView

# App config
SECRET_KEY: str = os.environ["NOTAS_SECRET"]

# Spreadhseet config
SERVICE_ACCOUNT_CREDENTIALS: str = os.environ["NOTAS_SERVICE_ACCOUNT_CREDENTIALS"]
SPREADSHEET_KEY: str = os.environ["NOTAS_SPREADSHEET_KEY"]

# Gmail config
EMAIL_ACCOUNT: str = os.environ['EMAIL_ACCOUNT']
EMAIL_PASSWORD: str = os.environ['EMAIL_PASSWORD']

# Flask configuration
app = flask.Flask(__name__)
app.secret_key = SECRET_KEY

# Infrastructure
signer = ItsDangerousSigner(SECRET_KEY)
email_sender = EmailMessageSender(EMAIL_ACCOUNT, EMAIL_PASSWORD, app.jinja_env)
student_repository = StudentRepositorySpreadsheet(
    service_account_credentials=json.loads(SERVICE_ACCOUNT_CREDENTIALS),
    spreadsheet_key=SPREADSHEET_KEY,
)

# Application Services
student_auth_service = StudentAuthService(
    student_repository, email_sender, signer)
grades_service = GradesService()

# Views
signin_view = SigninView.as_view(
    name='index',
    student_auth_service=student_auth_service,
    email_sender=email_sender
)
grades_view = GradesView.as_view(
    name='grades',
    signer=signer
)

# Endpoints
app.add_url_rule('/', view_func=signin_view)
app.add_url_rule('/grades/', view_func=grades_view)
