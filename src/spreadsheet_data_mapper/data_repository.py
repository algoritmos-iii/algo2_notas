from typing import List
import gspread

from .data_processors import (
    process_feedbacks,
    process_papers,
    process_students,
    process_groups,
    process_summary,
)
from .models import Group, Student, Paper, ExamFeedback, ExerciseFeedback, Summary, Exercise


class DataRepository:
    __slots__ = ["_spreadsheet", "students", "groups", "papers", "exercises", "exams", "summaries"]

    def __init__(self, spreadsheet_key: str, spreadsheet_auth_dict: dict) -> None:
        client = gspread.auth.service_account_from_dict(spreadsheet_auth_dict)
        self._spreadsheet = client.open_by_key(spreadsheet_key)

        # Data definitions
        self.students: List[Student] = []
        self.groups: List[Group] = []
        self.papers: List[Paper] = []
        self.exercises: List[ExerciseFeedback] = []
        self.exams: List[ExamFeedback] = []
        self.summaries: List[Summary] = []

    def _spreadsheet_values_batch_get(
        self, ranges: List[str], params: dict = None
    ) -> List[str]:
        data: dict = self._spreadsheet.values_batch_get(ranges, params=params)
        return [value_range["values"] for value_range in data["valueRanges"]]

    def get_data(self):
        (
            listado_raw,
            grupos_raw,
            papers_raw,
            ejercicios_raw,
            examenes_raw,
            summary_raw,
        ) = self._spreadsheet_values_batch_get(
            [
                "Listado!1:86",
                "Grupos!1:43",
                "Puntos extra papers!1:14",
                "Devoluciones",
                "Devoluciones examenes",
                "Alumnos - Notas!1:28",
            ],
            params={"majorDimension": "COLUMNS"},
        )

        self.summaries = [
            Summary(
                padron=data["identifier"],
                ejercicios=[
                    Exercise(
                        name="SAGA I",
                        grade=data["SAGA I"],
                    ),Exercise(
                        name="Codigo Repetido",
                        grade=data["Codigo Repetido"],
                    ),Exercise(
                        name="Números",
                        grade=data["Números"],
                    ),Exercise(
                        name="Stack",
                        grade=data["Stack"],
                    ),Exercise(
                        name="Mars Rover",
                        grade=data["Mars Rover"],
                    ),Exercise(
                        name="Servicios Financieros 1",
                        grade=data["Servicios Financieros 1"],
                    ),Exercise(
                        name="Servicios Financieros 2",
                        grade=data["Servicios Financieros 2"],
                    ),
                ],
                prom_ej=data["Promedio Ejercicios"],
                fist_parcial=data["1er Parcial"],
                prom_ej_1p=data["Ejercicios + 1er Parcial"],
                extra_papers=data["Extra Papers"],
                second_parcial=data["2do Parcial"],
                second_parcial_papers=data["2do Parcial + Papers"],
                first_recu=data["1er Recu"],
                first_recu_papers=data["1er Recu + Papers"],
                second_recu=data["2do Recu"],
                final_grade_secon_parcial=data["Nota Final 2do Parcial"],
                final_condition=data["Condición final"],
                grade_completed=data["Nota Cursada"],
                extra_point=data["Punto adicional"],
                grade_final_completed=data["Nota Cursada Final"],
                grade_promotion=data["Nota Promoción"],
            )
            for data in process_summary(summary_raw)
        ]

        # # print(process_summary(summary_raw))
        # for data in process_summary(summary_raw):
        #     print(data)

        self.students = [
            Student(
                padron=student["Padrón"],
                first_names=student["Nombre"].split(", ")[1],
                last_names=student["Nombre"].split(", ")[0],
                email=student["Email"],
            )
            for student in process_students(listado_raw)
        ]
        
        self.groups = [
            Group(
                group_number=group["Grupo"],
                padrones=[
                    val
                    for key, val in group.items()
                    if key in ["Padrón 1", "Padrón 2", "Padrón 3"] and val
                ],
                repository=group["Repo"],
            )
            for group in process_groups(grupos_raw)
        ]

        self.papers = [
            Paper(
                padron=paper["identifier"],
                papers={
                    key: value for key, value in paper.items() if key != "identifier"
                },
            )
            for paper in process_papers(papers_raw)
        ]

        self.exercises = [
            ExerciseFeedback(
                group_number=exercise["identifier"],
                exercise_name=exercise["activity_name"],
                grade=exercise["Nota"],
                corrector=exercise["Corrector"],
                details=exercise["Detalle"],
                email_sent=(exercise["EMAIL_SENT"] == "TRUE"),
                email_sent_position=exercise["email_sent_cell"],
            )
            for exercise in process_feedbacks(ejercicios_raw)
        ]

        self.exams = [
            ExamFeedback(
                student_padron=exam["identifier"],
                exam_name=exam["activity_name"],
                grade=exam["Nota"],
                extra_points=exam["Puntos extra"],
                final_grade=exam["Nota final"],
                corrector=exam["Corrector"],
                details=exam["Detalle"],
                email_sent=(exam["EMAIL_SENT"] == "TRUE"),
                email_sent_position=exam["email_sent_cell"],
            )
            for exam in process_feedbacks(examenes_raw)
        ]

        
    def write_to_exercise_sheet(self, cell: str, value: str):
        self._spreadsheet.worksheet("Devoluciones").update_acell(cell, value)

    def write_to_exam_sheet(self, cell:str, value: str):
        self._spreadsheet.worksheet("Devoluciones examenes").update_acell(cell, value)