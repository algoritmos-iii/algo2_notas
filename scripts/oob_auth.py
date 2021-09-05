#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Script para obtener el token de autorización de la aplicación.

El fichero “client_secrets.json” se obtiene de la cuenta tps.7540rw@gmail.com
en la URL:

  https://console.developers.google.com/project/1054797797536/apiui/credential

La URL que imprime el programa ha de ser abierta con la cuenta de Gmail
correspondiente a la asignatura (p.ej. tps.7541@gmail.com).
"""

import argparse

from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets


def get_credentials(client_secrets):
    """Autentica con OAuth2 a un usuario.

    Args:
        client_secrets: ruta al fichero “client_secrets.json” de la applicación.

    Returns:
        un objeto oauth2client.client.Credentials.
    """
    storage = Storage("/dev/null")

    flags = tools.argparser.parse_args(args=["--noauth_local_webserver"])
    flow = flow_from_clientsecrets(
        client_secrets,
        scope=["https://mail.google.com/",
               "https://spreadsheets.google.com/feeds"])

    return tools.run_flow(flow, storage, flags)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("client_secrets",
                        help="Ruta al fichero clients_secrets.json")

    args = parser.parse_args()
    credentials = get_credentials(args.client_secrets)

    # TODO(dato): también imprimir NOTAS_OAUTH_{CLIENT,SECRET}.
    print('NOTAS_REFRESH_TOKEN="%s"' % credentials.refresh_token)
    print('NOTAS_OAUTH_CLIENT="%s"' % credentials.client_id)
    print('NOTAS_OAUTH_SECRET="%s"' % credentials.client_secret)


if __name__ == "__main__":
    main()
