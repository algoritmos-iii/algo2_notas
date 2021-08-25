# Cambios a realizar

- [Actualizar la lib de google sheets](https://developers.google.com/sheets/api/quickstart/python)
    Se usa otra lib ( no oficial) --> https://docs.gspread.org/en/latest/oauth2.html
    Creo un proyecto `algo3-notas`
    Habilito google drive y sheets
- Conectar con nuestra planilla
- Icono

Para instalar todo `pipenv install --ignore-pipfile`
Antes ` . ./env` y luego:
`FLASK_ENV=development FLASK_APP=notasweb.py pipenv run flask run` para correr la app

- Queremos manejarnos tambien con el envio de mails? y un link?

- modificar func notas para adaptar a nuestra planilla de "Alumno - Notas" o adaptar planilla para que funcione con func que ya existe. 
    - Pensar si se quiere mostrar todo
    - Hacer planilla para que se pueda mostrar ?

- Cambiar template de html, alinearlo mejor a la pagina de la catedra


```json
{
    "nombre":"",
    "padron":"",
    "email":"",
    "ejercicios": {
        "Factorio":
        "... no seria dinamico"
    }
}

```