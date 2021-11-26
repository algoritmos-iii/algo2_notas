from grades.domain.models.correction import IndividualCorrection
from src.grades.application.grades_service import GradesService
from src.email.application.exam_email import ExamData, ExamEmail, ExamEmailData


class ExamsEmailView:
    def __init__(self, grades_service: GradesService, email_service: ExamEmail) -> None:
        self._grades_service = grades_service
        self._email_service = email_service

    def _generate_exam_data(
        self,
        exam_name: str,
        individual_correction: IndividualCorrection,
    ):
        return ExamEmailData(
            student_email=individual_correction.individual.email,
            exam_data=ExamData(
                exam_name=exam_name,
                student_full_name=individual_correction.individual.full_name,
                corrector_name=individual_correction.correction.corrector_name,
                correction_details=individual_correction.correction.details,
                grade=individual_correction.correction.grade,
                extra_points=individual_correction.exam_data["extra_points"],
                final_grade=individual_correction.exam_data["final_grade"],
            ),
        )

    def send(self, exam_name: str):
        for individual_correction in self._grades_service.get_exam_feedback_by_name(
            exam_name
        ):
            self._email_service.send_email(exam_name, individual_correction)

        return exam_name

    def preview(self, exam_name: str, padron_number: str):
        for individual_correction in self._grades_service.get_exam_feedback_by_name(
            exam_name
        ):
            if individual_correction.individual.padron == padron_number:
                return self._email_service.preview_email(
                    self._generate_exam_data(exam_name, individual_correction)
                )
        return "Not a valid padron"
