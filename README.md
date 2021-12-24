Pequeño sitio web que permite que los alumnos puedan consultar sus notas.

Los datos se obtienen de un google spreadsheet. El alumno especifica su padrón y e-mail, y si la dirección está asociada a ese padrón en el doc, se le envía un mail con un link exclusivo para que pueda consultar sus notas.

## Configuración y ejecución

Este proyecto utiliza la herramienta [`pipenv`](https://pipenv-es.readthedocs.io/es/latest/) para el manejo de bibliotecas.

Crear el ambiente virtual e instalar los requerimientos:

```bash
$ pipenv install
```

Crear un archivo llamado `.env` y poner los datos pertinentes:

```bash
NOTAS_COURSE_NAME='Algoritmos III - Leveroni'
NOTAS_SECRET='*****'

ADMIN_USERNAME='*****'
ADMIN_PASSWORD='*****'

EMAIL_ACCOUNT='*****'
EMAIL_PASSWORD='*****'

NOTAS_SERVICE_ACCOUNT_CREDENTIALS='******'
NOTAS_SPREADSHEET_KEY='*****'
```

Para más información acerca de cada variable, leer la sección _'Variables de entorno'_ debajo.

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

## Variables de entorno (archivo `.env`)

A continuación, pasamos a explicar las variables de entorno:

### Variables de la applicación

- `NOTAS_COURSE_NAME`: El nombre del curso.
- `NOTAS_SECRET`: Un string largo cuyo contenido debe mantenerse secreto. Se utiliza para firmas criptograficas que impiden la manipulación de cookies.

### Variables de webadmin

- `ADMIN_USERNAME` y `ADMIN_PASSWORD`: El nombre de usuario y la contraseña respectivamente para acceder a las funcionalidades de envio de emails.

### Variables de email

- `EMAIL_ACCOUNT` y `EMAIL_PASSWORD`: Es la cuenta de email de Google (gmail) y la contraseña para poder enviar mails desde esa cuenta.

### Variables de spreadsheet

- `NOTAS_SERVICE_ACCOUNT_CREDENTIALS`: Un string json conteniendo las credenciales del service account que permitira conectarse al spreadsheet.
- `NOTAS_SPREADSHEET_KEY`: Clave del spreadsheet al que se desea conectar.

## Features nuevos

Los nuevos PRs deben estar creados bajo el branch `develop`.

Para mas información, se puede mirar el siguiente [link](http://nvie.com/posts/a-successful-git-branching-model/).
