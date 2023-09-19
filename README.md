# Email sender

CLI que permite el envio de emails a los estudiantes con sus notas obtenidas de un google spreadsheet.


Configuración y ejecución
-------------------------

Este proyecto utiliza la herramienta [`pipenv`](https://pipenv-es.readthedocs.io/es/latest/) para el manejo de bibliotecas.

Crear el ambiente virtual e instalar los requerimientos:

```bash
$ pipenv install
```

Copiar el archivo `.env.example`, renombrarlo `.env` y completarlo.

Luego, correr el cli usando:
```bash
$ pipenv run cli

# O

$ python src/main.py
```

## Features nuevos

Los nuevos PRs deben estar creados bajo el branch `develop`.

Para mas información, se puede mirar el siguiente [link](http://nvie.com/posts/a-successful-git-branching-model/).
