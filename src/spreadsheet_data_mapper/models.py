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
class BaseFeedback:
    grade: str
    corrector: str
    detalle: str

@define
class ExamFeedback(BaseFeedback):
    padron: str
    name: str

@define
class ExerciseFeedback(BaseFeedback):
    grupo: str
    name: str
