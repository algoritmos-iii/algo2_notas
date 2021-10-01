Pequeño sitio web que permite que los alumnos puedan consultar sus notas.

Los datos se obtienen de un google spreadsheet. El alumno especifica su padrón y e-mail, y si la dirección está asociada a ese padrón en el doc, se le envía un mail con un link exclusivo para que pueda consultar sus notas.


Configuración y ejecución
-------------------------

Este proyecto utiliza la herramienta [`pipenv`](https://pipenv-es.readthedocs.io/es/latest/) para el manejo de bibliotecas.

Crear el ambiente virtual e instalar los requerimientos:

```bash
$ pipenv install
```

Crear un archivo llamado `.env` y poner los datos pertinentes:

```bash
NOTAS_COURSE_NAME='Algoritmos III - Leveroni'
NOTAS_ACCOUNT='*****@gmail.com'
NOTAS_SECRET='*****'
NOTAS_SPREADSHEET_KEY='*****'
NOTAS_SERVICE_ACCOUNT_JSON='./service_account.json'
NOTAS_OAUTH_CLIENT='*****'
NOTAS_OAUTH_SECRET='*****'
NOTAS_REFRESH_TOKEN='*****'
```

Solo es necesario completar todos los campos en caso de que se desee la funcionalidad completa. Para más información, leer la sección *'Variables de entorno'* debajo.


> Las instrucciones a continuación hablarán de como correr el programa en DEVELOPMENT. Las configuraciones no estarán optimizadas y pueden mostrarse información de errores que no se desee mostrar al publico. Esto solo es para pruebas de desarrollo.


Para correr el programa, es suficiente con correr Flask desde el entorno creado por pipenv:
> Los comandos siguientes suponen que el usuario esta parado en el directorio raiz del proyecto.

```bash
$ pipenv shell
$ flask run
```
Luego se puede mandar el comando `exit` para salir del entorno creado por pipenv, o cerrar la terminal directamente.

O si no se desea entrar y salir del entorno de pipenv, se puede ejecutar el programa usando `pipenv run` de la siguiente manera:

```bash
$ pipenv run flask run
```

Variables de entorno (archivo `.env`)
---------------------------------------

A continuación, pasamos a explicar las variables de entorno:

* `NOTAS_COURSE_NAME` es el nombre de la app.
* `NOTAS_ACCOUNT` y `NOTAS_SECRET` son credenciales de la cuenta.
* `NOTAS_SPREADSHEET_KEY` es el id del google spreadsheet que contiene la información.
* `NOTAS_SERVICE_ACCOUNT_JSON` es la ruta donde se encuenta el archivo `service_account.json`. Se explicará en más detalle como obtener ese archivo en la sección *'autenticación'*.
* `NOTAS_SECRET` y `NOTAS_OAUTH_SECRET` a todos los efectos practicos de este programa, comparten el mismo valor.
* Como se verá en la sección *'autenticación'*, el valor de `NOTAS_OAUTH_CLIENT`, `NOTAS_OAUTH_SECRET` y `NOTAS_REFRESH_TOKEN` puede ser extraido del archivo `service_account.json`.

Autenticación
-------------

El valor de `NOTAS_OAUTH_CLIENT`, `NOTAS_OAUTH_SECRET` y `NOTAS_REFRESH_TOKEN` se obtiene mediante OAuth2. Véase la documentación de `scripts/oob_auth.py`. Para utilizar el script, será necesario poseer un archivo llamado `clients_secrets.json` con la información adecuada.

## Features nuevos

Los nuevos PRs deben estar creados bajo el branch `develop`.

Para mas información, se puede mirar el siguiente [link](http://nvie.com/posts/a-successful-git-branching-model/).
