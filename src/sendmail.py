#!/usr/bin/env python3

import base64
import smtplib
import os
from email.mime.text import MIMEText

import notas_oauth

# para configurar desde afuera
COURSE = os.environ['NOTAS_COURSE_NAME']
ACCOUNT = os.environ['NOTAS_ACCOUNT']

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

def sendmail(fromname, toaddr, link):
	msg = MIMEText(template.format(enlace=link, curso=COURSE),
	               _charset="utf-8")
	msg["Subject"] = "Enlace para consultar las notas"
	msg["From"] = "{} <{}>".format(fromname, ACCOUNT)
	msg["To"] = toaddr

	creds = notas_oauth.get_credenciales_email()
	xoauth2_tok = "user={}\1" "auth=Bearer {}\1\1".format(
	    ACCOUNT, creds.access_token).encode("utf-8")
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.docmd("AUTH", "XOAUTH2 " +
	             base64.b64encode(xoauth2_tok).decode("utf-8"))
	server.sendmail(ACCOUNT, toaddr, msg.as_string())
	server.close()

