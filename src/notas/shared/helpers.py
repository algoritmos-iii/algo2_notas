def _string_to_snake_case(string: str) -> str:
    return string.lower().replace(" ", "_")


def _exercise_to_named_range(exercise_name: str) -> str:
    return "emails_" + _string_to_snake_case(exercise_name)
