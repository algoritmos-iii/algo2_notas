from src.grades.domain.models.correction import IndividualCorrection
from src.grades.application.grades_service import GradesService
from src.emails.application.exam_email_builder import ExamEmailBuilder, ExamData
from src.emails.domain.interfaces.email_sender_interface import (
    EmailSenderInterface,
)


class ExamsEmailView:
    def __init__(
        self,
        grades_service: GradesService,
        exam_email_builder: ExamEmailBuilder,
        email_sender: EmailSenderInterface,
    ) -> None:
        self._grades_service = grades_service
        self._exam_email_builder = exam_email_builder
        self._email_sender = email_sender

    def _generate_exam_data(self, exam_name: str, correction: IndividualCorrection):
        return ExamData(
            exam_name=exam_name,
            student_padron=correction.individual.padron,
            student_full_name=correction.individual.full_name,
            corrector_name=correction.correction.corrector_name,
            correction_details=correction.correction.details,
            grade=correction.correction.grade,
            extra_points=correction.exam_data["extra_points"],
            final_grade=correction.exam_data["final_grade"],
        )

    def send(self, exam_name: str):
        emails = [
            self._exam_email_builder.create_email(
                to_addr=correction.individual.email,
                data=self._generate_exam_data(exam_name, correction),
            )
            for correction in self._grades_service.get_not_sent_exam_feedback(exam_name)
        ]

        # TODO: add try catch for errors in email sending
        self._email_sender.send_multiple(emails)

        return exam_name

    def preview(self, exam_name: str, padron_number: str):
        for individual_correction in self._grades_service.get_exam_feedback(exam_name):
            if individual_correction.individual.padron == padron_number:
                exam_data = self._generate_exam_data(exam_name, individual_correction)
                return self._exam_email_builder.html_part(exam_data)

        return "Not a valid padron"
