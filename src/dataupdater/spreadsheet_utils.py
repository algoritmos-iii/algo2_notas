import unicodedata
from itertools import zip_longest


def _strip_accents(s):
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )


def normalize_header(string):
    return _strip_accents(string).replace(" ", "_").lower()


def spreadsheet_to_dict(data, filter_func=lambda _: True):
    headers = [normalize_header(header) for header in data.pop(0)]
    data_dict = [
        dict(zip_longest(headers, elem, fillvalue=""))
        for elem in data
        if filter_func(elem)
    ]

    return data_dict


def s_to_int_or_none(string: str):
    if not string.isnumeric():
        return None
    return int(string.replace(",", "."))


def s_to_float(string: str):
    return float(string.replace(",", ".").replace("#N/A", "nan"))
