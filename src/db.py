from typing import Optional
from pymongo import MongoClient
from config import MongoConfig

_mongo_config = MongoConfig()

_client = MongoClient(_mongo_config.url)
_db = _client["algo3_2c2022"]


def get_student_by_padron(padron: int):
    return _db["students"].find_one({"padron": padron})


def get_exercises_by_group(group: int, email_sent: Optional[bool] = None):
    query_filter = {"grupo": group}
    if email_sent is not None:
        query_filter["email_sent"] = email_sent

    return list(
        _db["exercises"].find(
            filter=query_filter,
            sort=[("_id", 1)],
        ),
    )


def get_exercise_by_group_and_name(group: int, name: str):
    return _db["exercises"].find_one({"grupo": group, "title": name})


def get_exams_by_padron(padron: int, email_sent: Optional[bool] = None):
    query_filter = {"padron": padron}
    if email_sent is not None:
        query_filter["email_sent"] = email_sent

    return list(
        _db["exams"].find(
            filter=query_filter,
            sort=[("_id", 1)],
        ),
    )


def get_exam_by_padron_and_name(padron: int, name: str):
    return _db["exams"].find_one({"padron": padron, "title": name})
