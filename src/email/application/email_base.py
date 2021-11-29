from typing import Any, Dict, Union

from ..domain.interfaces.message_sender_interface import MessageSenderInterface
from ..domain.interfaces.templater_interface import TemplaterInterface
from ..domain.models.message import EmailIntent


class EmailBase:
    TEMPLATE_PLAIN_DIR: str = None
    TEMPLATE_HTML_DIR: str = None
    WITH_COPY_TO_DOCENTES: bool = None

    def __init__(
        self,
        message_sender: MessageSenderInterface,
        templater: TemplaterInterface,
        docentes_email: str,
    ) -> None:
        assert self.TEMPLATE_PLAIN_DIR
        assert self.TEMPLATE_HTML_DIR
        assert self.WITH_COPY_TO_DOCENTES != None

        self._templater = templater
        self._docentes_email = docentes_email
        self._message_sender = message_sender

    def _render_plaintext(self, context: Dict[str, Any]):
        return self._templater.render(self.TEMPLATE_PLAIN_DIR, context)

    def _render_html(self, context: Dict[str, Any]):
        return self._templater.render(self.TEMPLATE_HTML_DIR, context)

    def _create_message(
        self,
        to_email_address: Union[str, list],
        subject: str,
        context: Dict[str, Any],
    ):
        return EmailIntent(
            to=to_email_address,
            subject=subject,
            reply_to=self._docentes_email,
            cc=self._docentes_email if self.WITH_COPY_TO_DOCENTES else None,
            plaintext_content=self._render_plaintext(context),
            html_content=self._render_html(context),
        )
