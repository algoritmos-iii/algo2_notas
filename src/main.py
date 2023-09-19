import click
from spreadsheet_data import get_all_data
from tabulate import tabulate
from dotenv import load_dotenv
from config import SpreadsheetConfig, EmailConfig
from emails.emails import Email, smtp_connection
from jinja2_env import jinja2_env

load_dotenv()

_spreadsheet_config = SpreadsheetConfig()
_email_config = EmailConfig()

click.echo("Getting data...", err=True)
_data = get_all_data(
    gspread_credentials=_spreadsheet_config.credentials,
    spreadsheet_key=_spreadsheet_config.spreadsheet_key,
)
click.echo("Data downloaded", err=True)


def _create_connection():
    return smtp_connection(
        server_address=_email_config.smtp_server_address,
        server_port=int(_email_config.smtp_server_port),
        account=_email_config.account,
        password=_email_config.password,
        use_ssl=False,
    )


@click.group
def cli():
    pass


@cli.command(help="Show the data that will be used")
@click.argument(
    "data_type",
    type=click.Choice(
        choices=["students", "exercises", "exams", "papers"],
        case_sensitive=False,
    ),
)
def show_data(data_type: str):
    click.echo(
        tabulate(
            _data[data_type],
            headers="keys",
            tablefmt="grid",
            maxcolwidths=30,
        )
    )


def _create_exercise_email(feedback):
    context = {
        "ejercicio": feedback.ejercicio,
        "grupo": feedback.grupo,
        "corrector": feedback.corrector,
        "nota": feedback.nota,
        "correcciones": feedback.detalle,
    }

    email = (
        Email(jinja2_env)
        .set_recipients(feedback.email)
        .set_from(_email_config.account)
        .set_subject(
            f"Correción de ejercicio {context['ejercicio']} - Grupo {context['grupo']}"
        )
        .set_cc(_email_config.docentes_email)
        .set_reply_to(_email_config.docentes_email)
        .set_plaintext_content_from_template(
            template_name="notas_ejercicio_plain.html",
            context=context,
        )
        .set_html_content_from_template(
            template_name="notas_ejercicio.html",
            context=context,
        )
    )

    email.metadata = context

    return email


@cli.command(help="Send the emails of specific exercise to students")
@click.argument("exercise_name", type=click.STRING)
@click.option(
    "--since-group",
    type=click.INT,
    default=None,
    help="Filter groups to only send those with a group number greater or equal to the one given",
)
def send_exercise_email(exercise_name: str, since_group: int | None):
    exercises = _data["exercises"]
    filtered_exercises = exercises[exercises["ejercicio"] == exercise_name].sort_values(
        by="grupo"
    )

    if since_group is not None:
        filtered_exercises = filtered_exercises[
            filtered_exercises["grupo"] >= since_group
        ]

    if len(filtered_exercises.index) <= 0:
        click.echo("There is nothing to send. Exiting...")
        click.echo("Remember that the exercise names are:", err=True)
        for exercise in _data["exercises"]["ejercicio"].unique():
            click.echo(f"- {exercise}", err=True)
        return

    emails = [
        _create_exercise_email(exercise) for exercise in filtered_exercises.itertuples()
    ]

    should_send = click.confirm(
        f"""The following data will be used:
- Exercise: {exercise_name}
- Amount of emails: {len(emails)}
- SMTP server: {_email_config.smtp_server_address}:{_email_config.smtp_server_port}
- Email account: {_email_config.account}
- Docentes email: {_email_config.docentes_email}"""
    )

    if not should_send:
        click.echo("Email sending aborted")
        return

    with _create_connection() as connection:
        for email in emails:
            group_number = email.metadata["grupo"]
            try:
                connection.send_message(email.generate_email_message())
            except Exception as e:
                click.echo(
                    f"Error sending mail of group {group_number}: {e}.",
                    err=True,
                )
                click.echo("Exiting...", err=True)
                return
            else:
                click.echo(f"Email for group {group_number} sent successfuly")

    click.echo("All done!")

# TODO: Esta funcion se copia para referencia, pero no esta terminada ni usable
# Inspirense en `_create_exercise_email` para rearmarla

#TODO: Faltaria crear algo semejante a `send_exercise_email` pero para examenes
def _create_exam_email(feedback):
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
            f"Corrección de {feedback['examen']} - Padrón {feedback['estudiante']['padron']}"
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

if __name__ == "__main__":
    cli()
