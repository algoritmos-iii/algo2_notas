import flask

admin_blueprint = flask.Blueprint("admin", __name__, template_folder="template")

@admin_blueprint.get('/emails/exercise/<exercise>/send')
def send_exercise_email(exercise: str):
    ...

@admin_blueprint.get('/emails/exam/<exam>/send')
def send_exam_email(exam: str):
    ...

@admin_blueprint.get('/emails/exercise/<exercise>/preview')
def preview_exercise_email(exercise: str):
    ...

@admin_blueprint.get('/emails/exam/<exam>/preview')
def preview_exam_email(exam: str):
    ...
