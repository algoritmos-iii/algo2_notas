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
