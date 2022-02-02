import itertools
from typing import Iterable


def _get_groups_indexes(column) -> tuple:
    """
    Indexes returned are 0-indexed.
    Assumes that first and last elements are not empty.
    """

    first_indexes = [0]
    last_indexes = []

    for index, elem in enumerate(column):
        if index > 0 and elem and not column[index - 1]:
            first_indexes.append(index)

        if index < len(column) - 1 and elem and not column[index + 1]:
            last_indexes.append(index)

    last_indexes.append(len(column) - 1)

    return tuple(zip(first_indexes, last_indexes))


def process_feedbacks(dataset: Iterable):

    [headers_col, *data_cols] = dataset
    [_, *data_groups] = _get_groups_indexes(headers_col)

    output = []

    for col in data_cols:
        identifier = col[0]

        for group_idx in data_groups:
            output.append(
                {
                    "identifier": identifier,
                    "activity_name": headers_col[group_idx[0]],
                    **dict(
                        itertools.zip_longest(
                            headers_col[group_idx[0] + 1 : group_idx[1] + 1],
                            [
                                field.strip()
                                for field in col[group_idx[0] + 1 : group_idx[1] + 1]
                            ],
                            fillvalue="",
                        ),
                    ),
                }
            )

    return output


def process_papers(dataset: Iterable):
    [headers_col, *data_cols] = dataset
    [_, *data_groups] = _get_groups_indexes(headers_col)

    output = []

    for col in data_cols:
        identifier = col[0]

        for group_idx in data_groups:
            output.append(
                {
                    "identifier": identifier,
                    **dict(
                        itertools.zip_longest(
                            headers_col[group_idx[0] : group_idx[1] + 1],
                            [
                                field.strip()
                                for field in col[group_idx[0] : group_idx[1] + 1]
                            ],
                            fillvalue="",
                        ),
                    ),
                }
            )

    return output


def process_students(dataset: Iterable):
    headers, *data = list(itertools.zip_longest(*dataset, fillvalue=None))
    return [dict(zip(headers, student)) for student in data]

def process_groups(dataset: Iterable):
    headers, *data = list(itertools.zip_longest(*dataset, fillvalue=None))
    return [dict(zip(headers, group)) for group in data]