import flask
from ..security import auth_required
from ..emails import smtp_connection, Email
from ..db import _db
from ..dataupdater import update_all

admin_blueprint = flask.Blueprint(
    name="admin",
    import_name=__name__,
    template_folder="template",
)


@admin_blueprint.get("/updatedb")
@auth_required
def updatedb():
    try:
        # Update db
        update_all()
    except Exception as ex:
        return flask.jsonify({"status": "error", "details": ex}), 400
    else:
        return flask.jsonify({"status": "ok"}), 200


# Emails
def create_exercise_email(feedback):
    emails = [integrante["email"] for integrante in feedback["integrantes"]]

    context = {
        "ejercicio": feedback["ejercicio"],
        "grupo": feedback["grupo"],
        "corrector": feedback["corrector"],
        "nota": feedback["nota"],
        "correcciones": feedback["detalle"],
    }

    return (
        Email()
        .set_recipients(",".join(emails))
        .set_subject(
            f"Correción de ejercicio {context['ejercicio']} - Grupo {context['grupo']}"
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


def create_exam_email(feedback):
    email = feedback["estudiante"]["email"]

    context = {
        "examen": feedback["examen"],
        "nombre": feedback["estudiante"]["nombre"],
        "corrector": feedback["corrector"],
        "correcciones": feedback["detalle"],
        "nota": feedback["nota"],
        "puntos_extras": feedback["puntos_extra"],
        "nota_final": feedback["nota_final"],
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


# Streaming function
def email_streaming_generator(emails, collection):
    with smtp_connection() as connection:

        for email in emails:
            email_sent_error = ""
            try:
                connection.send_message(email.generate_email_message())
            except Exception as e:
                email_sent_error = str(e)
            else:
                _db[collection].update_one(
                    filter={"_id": feedback["_id"]},
                    update={"$set": {"email_sent": True}},
                )

            yield f"{{address: {email._headers['to']}, subject: {email._headers['subject']}, email_sent: {not bool(email_sent_error)}}}\n"
    yield "Emails sent"


# Endpoints
@admin_blueprint.post("/emails/exercise/<exercise>/send")
@auth_required
def send_exercise_email(exercise: str):
    feedbacks = _db["exercises"].aggregate(
        [
            {"$match": {"ejercicio": exercise, "email_sent": False}},
            {
                "$lookup": {
                    "from": "students",
                    "localField": "grupo",
                    "foreignField": "grupo",
                    "as": "integrantes",
                    "pipeline": [{"$project": {"email": 1, "name": 1}}],
                }
            },
        ]
    )

    if not feedbacks:
        return f"Ejercicio {exercise} no encontrado o ya enviado"

    return flask.Response(
        flask.stream_with_context(
            email_streaming_generator(
                (create_exercise_email(feedback) for feedback in feedbacks),
                "exercises"
            )
        )
    )


@admin_blueprint.post("/emails/exam/<exam>/send")
@auth_required
def send_exam_email(exam: str):
    feedbacks = _db["exams"].aggregate(
        [
            {"$match": {"examen": exam, "email_sent": False}},
            {
                "$lookup": {
                    "from": "students",
                    "localField": "padron",
                    "foreignField": "padron",
                    "as": "estudiante",
                    "pipeline": [{"$project": {"_id": 0, "email": 1, "nombre": 1}}],
                }
            },
            {"$set": {"estudiante": {"$arrayElemAt": ["$estudiante", 0]}}},
        ]
    )

    if not feedbacks:
        return f"Examen {exam} no encontrado o ya enviado"

    return flask.Response(
        flask.stream_with_context(
            email_streaming_generator(
                (create_exam_email(feedback) for feedback in feedbacks),
                "exams"
            )
        )
    )
