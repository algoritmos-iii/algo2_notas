from pymongo import MongoClient
from config import MongoConfig

_mongo_config = MongoConfig()

_client = MongoClient(_mongo_config.url)
_db = _client["test"]


def get_student_by_padron(padron: int):
    return _db["students"].find_one({"padron": padron})


def get_exercises_by_group(group: int):
    return list(
        _db["exercises"].find(
            filter={"grupo": group},
            sort=[("_id", 1)],
        ),
    )


def get_exams_by_padron(padron: int):
    return list(
        _db["exams"].find(
            filter={"padron": padron},
            sort=[("_id", 1)],
        ),
    )


def get_exercise_by_group_and_name(group: int, name: str):
    return _db["exercises"].find_one({"grupo": group, "title": name})


def get_exam_by_padron_and_name(padron: int, name: str):
    return _db["exams"].find_one({"padron": padron, "title": name})
