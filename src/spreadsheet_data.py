import unicodedata
import gspread
import pandas as pd
from typing import TypedDict

Data = TypedDict(
    "data",
    {
        "students": pd.DataFrame,
        "exercises": pd.DataFrame,
        "exams": pd.DataFrame,
        "papers": pd.DataFrame,
    },
)


def _strip_accents(s):
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )


def _normalize_header(string):
    return _strip_accents(string).replace(" ", "_").lower()


def _to_dataframe(values):
    headers = [_normalize_header(header) for header in values[0]]
    df = pd.DataFrame(values[1:], columns=headers)
    return df.replace("", None).dropna()


def _to_numeric(data):
    return data.apply(lambda column: column.str.replace(",", ".")).apply(pd.to_numeric)


def get_all_data(gspread_credentials, spreadsheet_key):
    spreadsheet = gspread.service_account_from_dict(gspread_credentials).open_by_key(
        spreadsheet_key
    )

    students_raw, exercises_raw, exams_raw, papers_raw = spreadsheet.values_batch_get(
        ["Listado!B:E", "test-app!A:F", "test-app!K:S", "test-app!X:Y"],
        params={"majorDimension": "ROWS"},
    )["valueRanges"]

    students = _to_dataframe(students_raw["values"])
    exercises = _to_dataframe(exercises_raw["values"])
    exams = _to_dataframe(exams_raw["values"])
    papers = _to_dataframe(papers_raw["values"])

    # Filter and transform data
    students[["padron", "grupo"]] = _to_numeric(students[["padron", "grupo"]])
    exercises[["nota", "grupo"]] = _to_numeric(exercises[["nota", "grupo"]])
    exams[["nota", "puntos_extra", "nota_final", "padron"]] = _to_numeric(
        exams[["nota", "puntos_extra", "nota_final", "padron"]]
    )
    papers["winners"] = papers["winners"].str.split("\n").str[:-1]

    # Return data
    return Data(
        {
            "students": students,
            "exercises": exercises,
            "exams": exams,
            "papers": papers,
        }
    )
