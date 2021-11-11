import os
import json
import jinja2
import dotenv

from src.notas.infrastructure.email_message_sender import EmailMessageSender
from src.notas.infrastructure.student_repository_spreadsheet import (
    StudentRepositorySpreadsheet,
)
from src.notas.application.student_auth_service import StudentAuthService


dotenv.load_dotenv()

# Spreadhseet
SERVICE_ACCOUNT_CREDENTIALS: str = os.environ["NOTAS_SERVICE_ACCOUNT_CREDENTIALS"]
SPREADSHEET_KEY: str = os.environ["NOTAS_SPREADSHEET_KEY"]

# Gmail
EMAIL_ACCOUNT: str = os.environ['EMAIL_ACCOUNT']
EMAIL_PASSWORD: str = os.environ['EMAIL_PASSWORD']

env = jinja2.Environment(loader=jinja2.FileSystemLoader("./templates"))

student_repository = StudentRepositorySpreadsheet(
    service_account_credentials=json.loads(SERVICE_ACCOUNT_CREDENTIALS),
    spreadsheet_key=SPREADSHEET_KEY,
)
email_sender = EmailMessageSender(EMAIL_ACCOUNT, EMAIL_PASSWORD, env)
student_auth_service = StudentAuthService(student_repository, email_sender)

student = student_auth_service.find_student("jtaras@fi.uba.ar", "104728")
if not student:
    print("No student could be fount with this combination of email and padron")
    exit(-1)

print(student)

student_auth_service.send_login_message(student, "example.org")