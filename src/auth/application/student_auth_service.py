from typing import Optional

from ..domain.student import StudentInfo
from ..domain.student_repository_interface import StudentRepositoryInterface
from ..domain.message_sender_interface import MessageSenderInterface
from ..domain.messages.login_message import LoginMessage
from ...shared.domain.signer_interface import SignerInterface


class StudentAuthService:
    def __init__(
        self,
        student_repository: StudentRepositoryInterface,
        message_sender: MessageSenderInterface,
        signer: SignerInterface,
    ) -> None:
        self._student_repository = student_repository
        self._message_sender = message_sender
        self._signer = signer

    def find_student(self, email: str, padron: int) -> Optional[StudentInfo]:
        student_with_grades = self._student_repository.get_student_by_padron(padron)
        student_info = student_with_grades.student_info

        if (not student_info) or (student_info.email != email):
            return None

        return student_info

    def send_login_message(self, student: StudentInfo, base_link_notas: str):
        signed_padron = self._signer.sign(student.padron)
        link_notas = base_link_notas.format(signed_padron=signed_padron)
        message = LoginMessage(login_link=link_notas)
        
        self._message_sender.send(student, message)
