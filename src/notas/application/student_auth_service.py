from typing import Optional

from ..domain.student import StudentInfo
from ..domain.student_repository_interface import StudentRepositoryInterface
from ..domain.message_sender_interface import MessageSenderInterface
from ..domain.messages.login_message import LoginMessage


class StudentAuthService:
    def __init__(
        self,
        student_repository: StudentRepositoryInterface,
        message_sender: MessageSenderInterface,
    ) -> None:
        self._student_repository = student_repository
        self._message_sender = message_sender

    def _create_login_message(self, user_link: str):
        return LoginMessage(login_link=user_link)

    def find_student(self, email: str, padron: int) -> Optional[StudentInfo]:
        student_with_grades = self._student_repository.get_student_by_padron(padron)
        student_info = student_with_grades.student_info

        if (not student_info) or (student_info.email != email):
            return None

        return student_info

    def send_login_message(self, student: StudentInfo, user_link: str):
        message = self._create_login_message(user_link)
        self._message_sender.send(student, message)
