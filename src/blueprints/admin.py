import flask
from security import auth_required
from emails import smtp_connection, Email
from spreadsheet_data_mapper import DataMapper
from spreadsheet_data_mapper.models import ExamFeedback, ExerciseFeedback

data_mapper = DataMapper()

admin_blueprint = flask.Blueprint(
    name="admin",
    import_name=__name__,
    template_folder="template",
)

# Emails
def create_exercise_email(feedback: ExerciseFeedback):
    emails = data_mapper.emails_from_group(feedback.group_number)
    context = {
        "ejercicio": feedback.exercise_name,
        "grupo": feedback.group_number,
        "corrector": feedback.corrector,
        "nota": feedback.grade,
        "correcciones": feedback.details,
    }

    return (
        Email()
        .set_recipients(",".join(emails))
        .set_subject(
            f"Correción de ejercicio {feedback.exercise_name} - Grupo {feedback.group_number}"
        )
        .set_cc_to_lista_docente(True)
        .set_plaintext_content_from_template(
            template_name="emails/notas_ejercicio_plain.html",
            context=context,
        )
        .set_html_content_from_template(
            template_name="emails/notas_ejercicio.html",
            context=context,
        )
    )


def create_exam_email(feedback: ExamFeedback):
    email = data_mapper.student_by_padron(feedback.student_padron).email
    student = data_mapper.student_by_padron(feedback.student_padron)
    context = {
        "examen": feedback.exam_name,
        "nombre": student.full_name,
        "corrector": feedback.corrector,
        "correcciones": feedback.details,
        "nota": float(feedback.grade.replace(",", ".")),
        "puntos_extras": float(feedback.extra_points.replace(",", ".")),
        "nota_final": float(feedback.final_grade.replace(",", ".")),
    }

    return (
        Email()
        .set_recipients(email)
        .set_subject(
            f"Corrección de {feedback.exam_name} - Padrón {feedback.student_padron}"
        )
        .set_cc_to_lista_docente(True)
        .set_plaintext_content_from_template(
            template_name="emails/notas_examen_plain.html",
            context=context,
        )
        .set_html_content_from_template(
            template_name="emails/notas_examen.html",
            context=context,
        )
    )


# Endpoints
@admin_blueprint.get("/emails/exercise/<exercise>/send")
@auth_required
def send_exercise_email(exercise: str):
    data_mapper.repository.get_data()
    feedbacks = data_mapper.not_sent_exercises_feedback_by_name(exercise)
    if not feedbacks:
        return f"Ejercicio {exercise} no encontrado o ya enviado"

    def generate():
        with smtp_connection() as connection:
            print("hola")
            for feedback in feedbacks:
                email = create_exercise_email(feedback)
                email_sent_error = ""
                try:
                    connection.send_message(email.generate_email_message())
                except Exception as e:
                    email_sent_error = str(e)
                else:
                    data_mapper.write_to_exercise_sheet(
                        cell=feedback.email_sent_position,
                        value="TRUE",
                    )

                yield f"{{address: {email._headers['to']}, subject: {email._headers['subject']}, email_sent: {not bool(email_sent_error)}}}\n"
        yield "Emails sent"

    return flask.Response(flask.stream_with_context(generate()))


@admin_blueprint.get("/emails/exam/<exam>/send")
@auth_required
def send_exam_email(exam: str):
    data_mapper.repository.get_data()
    feedbacks = data_mapper.not_sent_exam_feedback_by_name(exam)
    if not feedbacks:
        return f"Examen {exam} no encontrado o ya enviado"

    def generate():
        with smtp_connection() as connection:
            for feedback in feedbacks:
                email = create_exam_email(feedback)
                email_sent_error = ""
                try:
                    connection.send_message(email.generate_email_message())
                except Exception as e:
                    email_sent_error = str(e)
                else:
                    data_mapper.write_to_exam_sheet(
                        cell=feedback.email_sent_position,
                        value="TRUE",
                    )

                yield f"{{address: {email._headers['to']}, subject: {email._headers['subject']}, email_sent: {not bool(email_sent_error)}}}\n"
        yield "Emails sent"

    return flask.Response(flask.stream_with_context(generate()))
