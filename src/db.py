from pymongo import MongoClient
from .config import MongoConfig

_mongo_config = MongoConfig()

_client = MongoClient(_mongo_config.url)
_db = _client.get_default_database()

def get_student_by_padron(padron: int):
    return _db["students"].find_one({"padron": padron})


def get_exercise_by_group_and_name(group: int, name: str):
    return _db["exercises"].find_one({"grupo": group, "ejercicio": name})


def get_exam_by_padron_and_name(padron: int, name: str):
    return _db["exams"].find_one({"padron": padron, "examen": name})


def get_student_data(padron: int):
    return (
        _db["students"]
        .aggregate(
            [
                {
                    "$match": {
                        "padron": padron,
                    }
                },
                {
                    "$lookup": {
                        "from": "papers",
                        "localField": "padron",
                        "foreignField": "winners",
                        "as": "papers",
                    }
                },
                {
                    "$lookup": {
                        "from": "exercises",
                        "localField": "grupo",
                        "foreignField": "grupo",
                        "as": "exercises",
                        "pipeline": [{"$match": {"email_sent": True}}],
                    }
                },
                {
                    "$lookup": {
                        "from": "exams",
                        "localField": "padron",
                        "foreignField": "padron",
                        "as": "exams",
                        "pipeline": [{"$match": {"email_sent": True}}],
                    }
                },
                {
                    "$project": {
                        "nombre": 1,
                        "padron": 1,
                        "email": 1,
                        "grupo": 1,
                        "papers": "$papers.title",
                        "exercises": {"ejercicio": 1, "nota": 1},
                        "exams": {
                            "$map": {
                                "input": "$exams",
                                "in": {
                                    "examen": "$$this.examen",
                                    "nota": "$$this.nota_final",
                                },
                            }
                        },
                    }
                },
            ]
        )
        .next()
    )
