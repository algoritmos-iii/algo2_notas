import gspread
from pymongo import MongoClient
import pymongo
from src.config import MongoConfig, SpreadsheetConfig
from .spreadsheet_utils import spreadsheet_to_dict, s_to_float, s_to_int_or_none


def update_all():
    spreadsheet = gspread.service_account_from_dict(
        SpreadsheetConfig().credentials
    ).open_by_key(SpreadsheetConfig().spreadsheet_key)

    mongo = MongoClient(MongoConfig().url)
    db = mongo["algo3_2c2022"]

    students_raw, exercises_raw, exams_raw = spreadsheet.values_batch_get(
        ["Listado!B:E", "test-app!A:F", "test-app!K:S"],
        params={"majorDimension": "ROWS"},
    )["valueRanges"]

    students = spreadsheet_to_dict(students_raw["values"])
    exercises = spreadsheet_to_dict(
        exercises_raw["values"],
        filter_func=lambda exercise: len(exercise) >= 6 and exercise[5].strip() != "",
    )
    exams = spreadsheet_to_dict(
        exams_raw["values"],
        filter_func=lambda exam: len(exam) >= 7 and exam[6].strip() != "",
    )

    # Filter and transform data
    for student in students:
        student["padron"] = s_to_int_or_none(student["padron"])
        student["grupo"] = s_to_int_or_none(student["grupo"])

    for exercise in exercises:
        exercise["nota"] = s_to_float(exercise["nota"])
        exercise["grupo"] = s_to_int_or_none(exercise["grupo"])

    for exam in exams:
        exam["nota"] = s_to_float(exam["nota"])
        exam["puntos_extra"] = s_to_float(exam["puntos_extra"])
        exam["nota_final"] = s_to_float(exam["nota_final"])
        exam["padron"] = s_to_int_or_none(exam["padron"])

    # Update db
    with mongo.start_session() as session:
        if students:
            db["students"].bulk_write(
                [
                    pymongo.UpdateOne(
                        filter={"padron": student["padron"]},
                        update={"$set": student},
                        upsert=True,
                    )
                    for student in students
                ],
                ordered=False,
                session=session,
            )
            print("Students updated")
        else:
            print("No students")

        if exercises:
            db["exercises"].bulk_write(
                [
                    pymongo.UpdateOne(
                        filter={
                            "grupo": exercise["grupo"],
                            "ejercicio": exercise["ejercicio"],
                        },
                        update={
                            "$set": exercise,
                            "$setOnInsert": {"email_sent": False},
                        },
                        upsert=True,
                    )
                    for exercise in exercises
                ],
                ordered=False,
                session=session,
            )
            print("Exercises updated")
        else:
            print("No exercises")

        if exams:
            db["exams"].bulk_write(
                [
                    pymongo.UpdateOne(
                        filter={"padron": exam["padron"], "examen": exam["examen"]},
                        update={"$set": exam, "$setOnInsert": {"email_sent": False}},
                        upsert=True,
                    )
                    for exam in exams
                ],
                ordered=False,
                session=session,
            )
            print("Exams updated")
        else:
            print("No exams")
