from attrs import define


@define
class Student:
    padron: str
    first_names: str
    last_names: str
    email: str

    @property
    def full_name(self) -> str:
        return f"{self.first_names} {self.last_names}"


@define
class Paper:
    padron: str
    papers: dict


@define
class Group:
    group_number: str
    padrones: list
    repository: str


@define
class ExerciseFeedback:
    group_number: str
    exercise_name: str
    grade: str
    corrector: str
    details: str
    email_sent: bool
    email_sent_position: str


@define
class ExamFeedback:
    student_padron: str
    exam_name: str
    grade: str
    extra_points: str
    final_grade: str
    corrector: str
    details: str
    email_sent: bool
    email_sent_position: str


@define
class Exercise:
    grade: str
    name: str

@define
class Summary:
    padron: str
    ejercicios: list[Exercise]
    prom_ej:str
    fist_parcial:str
    prom_ej_1p:str
    extra_papers:str
    second_parcial:str
    second_parcial_papers: str
    first_recu:str
    first_recu_papers:str
    second_recu:str
    final_grade_secon_parcial:str
    final_condition:str
    grade_completed:str
    extra_point:str
    grade_final_completed:str
    grade_promotion:str