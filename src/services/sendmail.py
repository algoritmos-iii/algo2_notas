#!/usr/bin/env python3
from __future__ import annotations

import base64
import smtplib
from email.mime.text import MIMEText

from api.google_credentials import GoogleCredentials

class EmailSender:
	template = """
Este es el link para consultar tus notas:
{enlace}

Nota: El enlace generado es único para tu padrón. No lo compartas con nadie (a menos
que quieras que otros puedan ver tus notas).

-- 
Recibiste este mensaje porque te inscribiste en el sistema de consulta de
notas de {curso}. Si no es así, te pedimos disculpas y por favor ingorá este mail.
"""
	SendmailException = smtplib.SMTPException

	def __init__(self, course: str, account: str, google_credentials: GoogleCredentials) -> None:
		self._course = course
		self._account = account
		self._google_credentials = google_credentials

	def sendmail(self, fromname: str, toaddr: str, link: str) -> None:
		msg = MIMEText(self.template.format(enlace=link, curso=self._course),
					_charset="utf-8")
		msg["Subject"] = "Enlace para consultar las notas"
		msg["From"] = "{} <{}>".format(fromname, self._account)
		msg["To"] = toaddr

		creds = self._google_credentials.get_credenciales_email()
		xoauth2_tok = "user={}\1" "auth=Bearer {}\1\1".format(
			self._account, creds.access_token).encode("utf-8")
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.ehlo()
		server.starttls()
		server.ehlo()
		server.docmd("AUTH", "XOAUTH2 " +
					base64.b64encode(xoauth2_tok).decode("utf-8"))
		server.sendmail(self._account, toaddr, msg.as_string())
		server.close()