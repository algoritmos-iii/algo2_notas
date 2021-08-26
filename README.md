Pequeño sitio web que permite que los alumnos puedan consultar sus notas.

Los datos se obtienen de un google spreadsheet. El alumno especifica su padrón y e-mail, y si la dirección está asociada a ese padrón en el doc, se le envía un mail con un link exclusivo para que pueda consultar sus notas.

**Requerimientos:** webpy, gdata, oauth2client

Configuración y ejecución
-------------------------

Crear el ambiente virtual e instalar los requerimientos:

```bash
  $ pipenv install --ignore-pipfile
```

Crear un archivo llamado `env`:

```bash
export NOTAS_COURSE_NAME="Algoritmos I"
export NOTAS_ACCOUNT='xxxx@gmail.com'
export NOTAS_OAUTH_CLIENT='****'
export NOTAS_OAUTH_SECRET='****'
export NOTAS_REFRESH_TOKEN='****'
export NOTAS_SPREADSHEET_KEY='*****'
export NOTAS_SECRET='*****'
```

Es suficiente con correr Flask desde el entorno creado por pipenv:

```bash
$ . ./env
$ pipenv shell
$ FLASK_ENV=development FLASK_APP=notasweb.py flask run
```

O se puede usar pipenv run si no se desea modificar el shell:

```bash
  $ . ./env
  $ FLASK_ENV=development FLASK_APP=notasweb.py pipenv run flask run
```

Alternativamente, mediante contenedores de [Docker][], completar las credenciales en el archivo `docker.auth`, y ejecutar:

```bash
$ docker build -t fiuba/notas .
$ docker run --env-file docker.auth -p 8080:8080 --name notas.run fiuba/notas
```

  [docker]: https://www.docker.com

Autenticación
-------------

El valor de `NOTAS_REFRESH_TOKEN` se obtiene mediante OAuth2. Véase la documentación de `oob_auth.py`.
