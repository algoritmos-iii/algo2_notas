from .data_repository import DataRepository

from config import SpreadsheetConfig

spreadsheet_config = SpreadsheetConfig()


class DataMapper:
    repository = DataRepository(
        spreadsheet_config.spreadsheet_key,
        spreadsheet_config.spreadsheet_auth_dict,
    )

    # Groups

    def all_groups(self):
        return [
            group
            for group in self.repository.groups
            if group.group_number and len(group.padrones) > 0
        ]

    def all_group_numbers(self):
        return [group.group_number for group in self.all_groups()]

    def group_by_number(self, group_number: str):
        for group in self.all_groups():
            if group.group_number == group_number:
                return group
        return None

    def group_of_student(self, padron: str):
        for group in self.all_groups():
            if padron in group.padrones:
                return group
        return None

    def emails_from_group(self, group_number: str):
        for group in self.all_groups():
            if group.group_number == group_number:
                return [
                    self.student_by_padron(padron).email for padron in group.padrones
                ]
        return None

    # Papers

    def papers_of_student(self, padron: str):
        for paper_data in self.repository.papers:
            if paper_data.papers == padron:
                return [
                    paper_name
                    for paper_name, completed in paper_data.papers.items()
                    if completed == "1"
                ]

        return None

    # Exercises

    def _valid_exercises_feedback(self):
        return [
            exercise
            for exercise in self.repository.exercises
            if exercise.details and exercise.group_number in self.all_group_numbers()
        ]

    def all_exercises_feedback_by_name(self, exercise_name: str):
        return [
            exercise
            for exercise in self._valid_exercises_feedback()
            if exercise.exercise_name == exercise_name
        ]

    def not_sent_exercises_feedback_by_name(self, exercise_name: str):
        return [
            exercise
            for exercise in self.all_exercises_feedback_by_name(exercise_name)
            if not exercise.email_sent
        ]

    def exercises_feedback_by_group_number(self, group_number: str):
        return [
            exercise
            for exercise in self._valid_exercises_feedback()
            if exercise.group_number == group_number
        ]

    def write_to_exercise_sheet(self, cell: str, value: str):
        self.repository.write_to_exercise_sheet(cell, value)

    # Exams

    def _valid_exam_feedbacks(self):
        return [exam for exam in self.repository.exams if exam.details]

    def all_exam_feedback_by_name(self, exam_name: str):
        return [
            exam
            for exam in self.repository.exams
            if exam.exam_name == exam_name and exam.details
        ]

    def not_sent_exam_feedback_by_name(self, exam_name: str):
        return [
            exam
            for exam in self.all_exam_feedback_by_name(exam_name)
            if not exam.email_sent
        ]

    def exams_feedback_by_student(self, padron: str):
        return [
            exam
            for exam in self._valid_exam_feedbacks()
            if exam.student_padron == padron
        ]

    def write_to_exam_sheet(self, cell: str, value: str):
        self.repository.write_to_exam_sheet(cell, value)

    # Students

    def all_students(self):
        return [
            student
            for student in self.repository.students
            if student.padron and student.email
        ]

    def student_by_padron(self, padron: str):
        for student in self.all_students():
            if student.padron == padron:
                return student
        return None
